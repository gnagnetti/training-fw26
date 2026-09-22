#!/usr/bin/env python3
"""Merge the native CSV translations into the existing per-model JSON files.

Only the text dictionaries are rewritten (description / advice / objections /
look texts and titles). Everything that cannot come from the CSV (colors, look
items, image URLs, model ids) is left untouched, so a re-run never destroys work
already done.

Styling / Abbinamenti exists only in two columns in the CSV: the base (Russian)
one and the "Eng" one, so:
  * ru -> Russian segments
  * every other language -> the English segments (same content, translated)
The segments are aligned to the existing looks by garment codes + model names.

Mapping lingua -> suffisso colonna CSV (la colonna senza suffisso e' il Russo):
    ru -> ""      en -> "Eng"    ar -> "Ara"    ka -> "Geo"    hy -> "Arm"
    lv -> "Let"   lt -> "Lit"    pl -> "Pol"    uk -> "Ukr"
"""

import csv
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_universal_objections import parse_universal_objections  # noqa: E402

CSV_PATH = "226FWCollectionMultilingua.csv"
MODELS_DIR = "src/data/models"

LANG_COLUMNS = {
    "ru": "",
    "en": "Eng",
    "ar": "Ara",
    "ka": "Geo",
    "hy": "Arm",
    "lv": "Let",
    "lt": "Lit",
    "pl": "Pol",
    "uk": "Ukr",
}
# Styling exists only as Russian (base) + English; every non-Russian language
# shows the English text.
STYLING_LANGS_FROM_EN = [l for l in LANG_COLUMNS if l != "ru"]

MARKDOWN_IMAGE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
WORD_IMAGE_DIRECTIVE = re.compile(r"\.?\s*!\[([^\]]*)\]\([^)]+\)\s*\{[^}]*\}")
PAREN_URL = re.compile(r"\(\s*(?:https?://)[^()]*(?:\([^()]*\)[^()]*)*\)")
BARE_URL = re.compile(r"https?://\S+")

ITEM_RE = re.compile(r"\b([A-ZА-Я][A-Za-z0-9]{2,}(?:\s+[A-Z]\b)?)((?:\s+\d{3,4})+)")
VARIANT_RE = re.compile(r"\bВариант\s+[\d\s]+\s*:", re.I)
COMBINATION_RE = re.compile(
    r"(?:В\s+lookbook(?:\s*\([^)]*\))?|На\s+витрин(?:е|ах)(?:\s*\([^)]*\))?"
    r"|Lookbook(?:\s*\([^)]*\))?|Vetrina(?:\s*\([^)]*\))?"
    r"|Визуальный\s+мерчандайзинг(?:\s*\([^)]*\))?)\s*:",
    re.I,
)
DASH_COMBINATION_RE = re.compile(
    r"\s+-\s+(?=[^:]{0,100}(?:Look(?:book)?|Vetrina|В\s+lookbook|На\s+витрин|Витрин)[^:]{0,60}:)",
    re.I,
)
LOOK_HEAD_RE = re.compile(r"^([^:]{0,60}?):\s*(.*)$", re.S)
LOOK_HEAD_KEYWORDS = r"(Total Look|Vetrina|Стилистическое|Look|Styling|In the|Вариант)"


def clean(text: str) -> str:
    """Same tidying used by build_data.py for descriptions."""
    if not isinstance(text, str):
        return ""
    t = PAREN_URL.sub("", text)
    t = BARE_URL.sub("", t)
    t = WORD_IMAGE_DIRECTIVE.sub("", t)
    t = MARKDOWN_IMAGE.sub("", t)
    t = re.sub(r"\(\s*(nan|Данные отсутствуют[^)]*|URL non disponibile)\s*\)", "", t, flags=re.I)
    t = re.sub(r"\(\s*\)", "", t)
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)
    t = re.sub(r"([,.;:])\s*([,.;:])+", r"\1", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip(" ,;")


def split_pipe(raw) -> list[str]:
    if not isinstance(raw, str):
        return []
    return [clean(p) for p in raw.split("|") if p and p.strip()]


def parse_objections(raw, lang):
    return parse_universal_objections(raw, lang)


# ------------------------------------------------------------------ looks
def split_look_segments(raw: str) -> list[str]:
    """Same segmentation the build script used to create one look per entry."""
    cleaned = clean(raw)
    if not cleaned:
        return []
    parts = [p.strip() for p in re.split(r"\s*\|\s*", cleaned) if p.strip()]
    out: list[str] = []
    for part in parts:
        dash_starts = [m.end() for m in DASH_COMBINATION_RE.finditer(part)]
        explicit_starts = [
            m.start()
            for m in COMBINATION_RE.finditer(part)
            if not any(0 <= m.start() - ds <= 120 for ds in dash_starts)
        ]
        combinations = sorted(set(explicit_starts + dash_starts))
        if len(combinations) < 2:
            out.append(part)
            continue
        combinations = [
            s
            for i, s in enumerate(combinations)
            if not (i + 1 < len(combinations) and not part[s : combinations[i + 1]].strip(" -,:;"))
        ]
        variants = list(VARIANT_RE.finditer(part))
        intro = part[: combinations[0]].strip(" -,")
        for index, start in enumerate(combinations):
            next_start = combinations[index + 1] if index + 1 < len(combinations) else len(part)
            next_variant = next((v for v in variants if start <= v.start() < next_start), None)
            end = next_variant.start() if next_variant else next_start
            active_variant = next((v for v in reversed(variants) if v.start() < start), None)
            variant_text = active_variant.group(0).strip() if active_variant else ""
            body = part[start:end].strip(" -,")
            prefix = " ".join(x for x in (intro if index == 0 else "", variant_text if index > 0 else "") if x)
            segment = f"{prefix} {body}".strip()
            content_without_context = VARIANT_RE.sub("", segment).strip(" -,")
            if segment and not COMBINATION_RE.fullmatch(content_without_context):
                out.append(segment)
    return out


def _codes(text: str) -> set[str]:
    return set(re.findall(r"\d{3,4}", text))


def _item_names(text: str) -> set[str]:
    return {m.group(1).lower() for m in ITEM_RE.finditer(text)}


def _similarity(a: str, b: str) -> float:
    if a == b:
        return 1.0
    ca, na = _codes(a), _item_names(a)
    cb, nb = _codes(b), _item_names(b)
    jaccard = len(ca & cb) / max(1, len(ca | cb))
    name_bonus = 0.5 if (na and nb and na & nb) else 0.0
    return jaccard + name_bonus


def _best_match(target: str, candidates: list[str], excluded: set[int], threshold: float) -> int | None:
    best, best_score = None, -1.0
    for i, cand in enumerate(candidates):
        if i in excluded:
            continue
        score = _similarity(target, cand)
        if score > best_score:
            best, best_score = i, score
    if best is None or best_score < threshold:
        return None
    return best


def _align_by_content(sources: list[str], targets: list[str], threshold: float) -> dict[int, int]:
    """source index -> target index, keeping the original order for leftovers."""
    mapping: dict[int, int] = {}
    used: set[int] = set()
    for i, src in enumerate(sources):
        hit = _best_match(src, targets, used, threshold)
        if hit is not None:
            mapping[i] = hit
            used.add(hit)
    free = [i for i in range(len(targets)) if i not in used]
    for i in range(len(sources)):
        if i not in mapping and free:
            mapping[i] = free.pop(0)
    return mapping


def _split_head(segment: str) -> tuple[str | None, str]:
    head = LOOK_HEAD_RE.match(segment)
    if head and re.search(LOOK_HEAD_KEYWORDS, head.group(1), re.I):
        return head.group(1).strip(), head.group(2)
    return None, segment


def _translate_segment(segment: str, source_segments: list[str], translated_segments: list[str]) -> str:
    """Return the counterpart of `segment` inside `translated_segments`."""
    if not translated_segments:
        return ""
    exact = _align_by_content([segment], translated_segments, 0.999)
    idx = exact.get(0)
    if idx is None:
        idx = _align_by_content([segment], translated_segments, 0.2).get(0)
    if idx is None:
        return ""
    return translated_segments[idx]


def _is_genuinely_english(text: str) -> bool:
    """The Eng column sometimes just repeats the Russian text (see ID 422-431)."""
    if not text:
        return False
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    cyrillic = sum(1 for c in letters if "Ѐ" <= c <= "ӿ")
    return cyrillic / len(letters) < 0.15


def merge_looks(model: dict, row: dict) -> dict:
    """Give every look a per-language text/title dictionary.

    Rules (from the source spreadsheet):
      * ru  -> the Russian segments of `Styling / Abbinamenti`, with the section
               tag kept as the look title and removed from the body (no language
               tags left inside the text).
      * every other language -> the segments of `Styling / Abbinamenti Eng`.
               When the Eng column is not really English (a few models just copy
               the Russian text), we fall back to the same Russian text so the
               section is never empty.
    """
    looks = model.get("looks") or []
    if not looks:
        return model

    ru_raw = (row.get("Styling / Abbinamenti") or "").strip()
    en_raw = (row.get("Styling / Abbinamenti Eng") or "").strip()
    ru_segs = split_look_segments(ru_raw) if ru_raw else []
    en_segs = split_look_segments(en_raw) if en_raw else []
    en_is_english = _is_genuinely_english(en_raw)

    # align each existing look with the Russian segments
    look_to_ru: dict[int, int] = {}
    if ru_segs and len(ru_segs) == len(looks):
        for li, lk in enumerate(looks):
            current = lk.get("text")
            text = current if isinstance(current, str) else ""
            if not text and isinstance(current, dict):
                text = current.get("ru") or current.get("en") or ""
            hit = None
            if text:
                hit = _best_match(text, ru_segs, set(), 0.999)
                if hit is None:
                    hit = _best_match(text, [_split_head(s)[1] for s in ru_segs], set(), 0.999)
                if hit is None:
                    hit = _best_match(text, ru_segs, set(), 0.2)
            if hit is None:
                hit = _best_match(
                    " ".join(it.get("name", "") for it in lk.get("items", [])),
                    ru_segs,
                    set(),
                    0.1,
                )
            if hit is not None:
                look_to_ru[li] = hit

    ru_to_en = _align_by_content(ru_segs, en_segs, 0.2) if ru_segs and en_segs else {}

    for li, lk in enumerate(looks):
        current_text = lk.get("text")
        current_title = lk.get("title")

        text_dict: dict[str, str] = dict(current_text) if isinstance(current_text, dict) else {}
        title_dict: dict[str, str | None] = (
            dict(current_title) if isinstance(current_title, dict) else {}
        )

        ri = look_to_ru.get(li)
        if ri is None:
            # no Russian counterpart found: keep what is stored and mirror it
            if isinstance(current_text, str) and current_text:
                text_dict["ru"] = current_text
            if isinstance(current_title, str) and current_title:
                title_dict["ru"] = current_title
            for lang in STYLING_LANGS_FROM_EN:
                text_dict.setdefault(lang, text_dict.get("ru", ""))
                title_dict.setdefault(lang, title_dict.get("ru"))
            if text_dict:
                lk["text"] = text_dict
            if title_dict:
                lk["title"] = title_dict
            continue

        ru_seg = ru_segs[ri]
        ru_head, ru_body = _split_head(ru_seg)

        ei = ru_to_en.get(ri)
        en_seg = en_segs[ei] if en_segs and ei is not None else ""
        en_head, en_body = _split_head(en_seg) if en_seg else (None, "")
        if not en_is_english:
            # the Eng column is Russian for this model: keep RU for every language
            en_head, en_body = ru_head, ru_body

        # Russian: tag becomes the title, body carries no language tags
        text_dict["ru"] = ru_body or ru_seg
        title_dict["ru"] = ru_head

        # every other language: English column
        for lang in STYLING_LANGS_FROM_EN:
            text_dict[lang] = en_body or en_seg or text_dict["ru"]
            title_dict[lang] = en_head

        lk["text"] = text_dict
        lk["title"] = title_dict if title_dict else lk.get("title")

    model["looks"] = looks
    return model


ALL_LANGS = ["en", "ru", "ar", "hy", "ka", "uk", "lv", "lt", "pl"]


def load_csv_rows() -> dict[int, dict]:
    with open(CSV_PATH, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        out = {}
        for row in reader:
            raw_id = (row.get("ID") or "").strip()
            if not raw_id:
                continue
            try:
                out[int(raw_id)] = row
            except ValueError:
                continue
        return out


def build_fallbacks(row: dict, field: str) -> dict[str, str]:
    """Empty values fall back to English, then to the Russian (base) column."""
    base = (row.get(field) or "").strip()
    eng = (row.get(f"{field} Eng") or "").strip()
    return {"base": base, "eng": eng}


def merge_model(path: str, csv_rows: dict[int, dict]) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        model = json.load(f)

    row = csv_rows.get(model["id"])
    if not row:
        return model

    # ---------------- description
    desc_fb = build_fallbacks(row, "Descrizione")
    description = dict(model.get("description") or {})
    for lang, suffix in LANG_COLUMNS.items():
        if suffix:
            val = (row.get(f"Descrizione {suffix}") or "").strip()
        else:
            val = desc_fb["base"]
        if not val:
            val = desc_fb["eng"] if lang != "en" else desc_fb["base"]
        if not val:
            val = desc_fb["base"]
        description[lang] = clean(val) if val else ""
    model["description"] = description

    # ---------------- sales advice
    adv_fb = build_fallbacks(row, "Consigli di Vendita")
    advice = dict(model.get("advice") or {})
    for lang, suffix in LANG_COLUMNS.items():
        if suffix:
            val = (row.get(f"Consigli di Vendita {suffix}") or "").strip()
        else:
            val = adv_fb["base"]
        if not val:
            val = adv_fb["eng"] if lang != "en" else adv_fb["base"]
        if not val:
            val = adv_fb["base"]
        items = split_pipe(val) if val else []
        advice[lang] = items
    model["advice"] = advice

    # ---------------- objection handling
    obj_fb = build_fallbacks(row, "Gestione Obiezioni")
    objections = dict(model.get("objections") or {})
    for lang, suffix in LANG_COLUMNS.items():
        if suffix:
            raw = (row.get(f"Gestione Obiezioni {suffix}") or "").strip()
        else:
            raw = obj_fb["base"]
        if not raw:
            raw = obj_fb["eng"] if lang != "en" else obj_fb["base"]
        if not raw:
            raw = obj_fb["base"]
        parsed = parse_objections(raw, lang) if raw else []
        objections[lang] = parsed
    model["objections"] = objections

    # ---------------- styling / looks
    model = merge_looks(model, row)

    return model


def export_aggregates(models: list[dict]) -> None:
    with open("src/data/models.json", "w", encoding="utf-8") as f:
        json.dump(models, f, ensure_ascii=False)

    os.makedirs("src/locales", exist_ok=True)
    for lang in ALL_LANGS:
        locale_data = {"lang": lang, "models": {}}
        for m in models:
            m_id = str(m["id"])
            desc = m.get("description", {}).get(lang) or m.get("description", {}).get("en") or ""
            adv = m.get("advice", {}).get(lang) or m.get("advice", {}).get("en") or []
            obj = m.get("objections", {}).get(lang) or m.get("objections", {}).get("en") or []
            lks = []
            for lk in m.get("looks", []):
                t_title = None
                if lk.get("title"):
                    if isinstance(lk["title"], dict):
                        t_title = lk["title"].get(lang) or lk["title"].get("en")
                    else:
                        t_title = lk["title"]
                t_text = ""
                if lk.get("text"):
                    if isinstance(lk["text"], dict):
                        t_text = lk["text"].get(lang) or lk["text"].get("en") or ""
                    else:
                        t_text = lk["text"]
                lks.append({"title": t_title, "text": t_text})

            locale_data["models"][m_id] = {
                "name": m["name"],
                "description": desc,
                "looks": lks,
                "advice": adv,
                "objections": obj,
            }

        with open(f"src/locales/{lang}.json", "w", encoding="utf-8") as f:
            json.dump(locale_data, f, ensure_ascii=False, indent=2)

    print("Exported src/data/models.json and src/locales/*.json")


def main() -> None:
    csv_rows = load_csv_rows()
    if not csv_rows:
        print(f"No rows loaded from {CSV_PATH}")
        return

    files = sorted(
        glob.glob(f"{MODELS_DIR}/*.json"),
        key=lambda p: int(os.path.basename(p).split(".")[0]),
    )
    print(f"Merging {len(files)} models with CSV translations...")

    models = []
    for path in files:
        model = merge_model(path, csv_rows)
        models.append(model)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(model, f, ensure_ascii=False, indent=2)

    export_aggregates(models)
    print(f"Done: {len(models)} models updated.")


if __name__ == "__main__":
    main()
