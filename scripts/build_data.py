"""Converts the source Excel files into src/data/models.json.

Run: python3 scripts/build_data.py <models.xlsx> <url.xlsx>
The image lookup (url.xlsx) is the single source of truth for every picture.
"""

import json
import re
import sys
from collections import defaultdict
from urllib.parse import quote

import pandas as pd

MODELS_XLSX, URL_XLSX = sys.argv[1], sys.argv[2]
OUT = "src/data/models.json"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", str(s)).strip().lower()


def enc(url: str | None) -> str | None:
    """Percent-encode spaces etc. so every image URL is loadable as-is."""
    return None if not url else quote(url, safe=":/%?&=#+,~@!$'*;")



def codes_key(codes) -> str:
    return " ".join(codes)


# ---------------------------------------------------------------- image index
def base(n: str) -> str:
    """'manos f' -> 'manos' (url.xlsx appends a one-letter line suffix)."""
    return re.sub(r"\s+[a-z]$", "", n).strip()


url_df = pd.read_excel(URL_XLSX)
by_full = {}
by_name = defaultdict(list)
for _, row in url_df.iterrows():
    raw = str(row["ModelloColore"])
    url = row["Style Image URL_1"]
    url = None if (pd.isna(url) or not str(url).startswith("http")) else enc(str(url).strip())
    m = re.match(r"^(.*?)\s*\(([\d\s]+)\)\s*$", raw)
    if not m:
        continue
    name, codes = norm(m.group(1)), re.findall(r"\d+", m.group(2))
    if not url:
        continue
    for n in {name, base(name)}:
        by_full.setdefault(f"{n}|{codes_key(codes)}", url)
        for c in codes:
            by_full.setdefault(f"{n}|{c}", url)
        by_name[n].append(url)

unmatched = defaultdict(int)


def lookup(name: str, codes) -> str | None:
    n = norm(name)
    for key in (n, base(n)):
        if codes:
            hit = by_full.get(f"{key}|{codes_key(codes)}")
            if hit:
                return hit
            for c in codes:
                hit = by_full.get(f"{key}|{c}")
                if hit:
                    return hit
        if by_name.get(key):
            return by_name[key][0]
    unmatched[f"{name} ({' '.join(codes)})"] += 1
    return None



# ---------------------------------------------------------------- text tidying
PAREN_URL = re.compile(r"\(\s*(?:https?://)[^()]*(?:\([^()]*\)[^()]*)*\)")
BARE_URL = re.compile(r"https?://\S+")
# Markdown image syntax: ![...](url) or ![](url)
MARKDOWN_IMAGE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
# HTML/Word image directives with attributes: ![](media/...) or similar with {...}
WORD_IMAGE_DIRECTIVE = re.compile(r"\.?\s*!\[([^\]]*)\]\([^)]+\)\s*\{[^}]*\}")


def clean(text: str) -> str:
    t = PAREN_URL.sub("", text)
    t = BARE_URL.sub("", t)
    # Remove Word/Markdown image directives first (they may contain {...} attributes)
    t = WORD_IMAGE_DIRECTIVE.sub("", t)
    # Remove any remaining Markdown image syntax
    t = MARKDOWN_IMAGE.sub("", t)
    t = re.sub(r"\(\s*(nan|Данные отсутствуют[^)]*|URL non disponibile)\s*\)", "", t, flags=re.I)
    t = re.sub(r"\(\s*\)", "", t)
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)
    t = re.sub(r"([,.;:])\s*([,.;:])+", r"\1", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip(" ,;")


ITEM_RE = re.compile(
    r"\b([A-ZА-Я][A-Za-z0-9]{2,}(?:\s+[A-Z]\b)?)((?:\s+\d{3,4})+)"
)


SKIP_NAMES = {"vetrina", "look", "total look", "total", "outfit"}


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


def split_look_segments(raw):
    """Split prose into one block per explicitly cited look/window display."""
    cleaned = clean(raw)
    parts = [p.strip() for p in re.split(r"\s*\|\s*", cleaned) if p.strip()]
    out = []

    for part in parts:
        dash_starts = [m.end() for m in DASH_COMBINATION_RE.finditer(part)]
        explicit_starts = [
            m.start()
            for m in COMBINATION_RE.finditer(part)
            if not any(0 <= m.start() - dash_start <= 120 for dash_start in dash_starts)
        ]
        # Prefer the dash boundary when it introduces a descriptive title whose
        # parenthetical Look/Vetrina label appears later in the same heading.
        combinations = sorted(set(explicit_starts + dash_starts))
        if len(combinations) < 2:
            out.append(part)
            continue

        # Container labels such as "На витринах (Vetrina):" introduce a list
        # but are not combinations themselves when followed by a concrete item.
        combinations = [
            start
            for index, start in enumerate(combinations)
            if not (
                index + 1 < len(combinations)
                and not part[start:combinations[index + 1]].strip(" -,.:;")
            )
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


def parse_looks(raw, self_name):
    if not isinstance(raw, str) or not raw.strip():
        return []
    looks = []
    for seg in split_look_segments(raw):
        seg = seg.strip()
        if not seg:
            continue
        title, body = None, seg
        head = re.match(r"^([^:]{0,60}?):\s*(.*)$", seg, flags=re.S)
        if head and re.search(r"(Total Look|Vetrina|Стилистическое|Look)", head.group(1), re.I):
            title, body = head.group(1).strip(), head.group(2)
        items, seen = [], set()
        body_clean = clean(body)
        for m in ITEM_RE.finditer(body_clean):
            name = re.sub(r"\s+", " ", m.group(1)).strip()
            if norm(name) in SKIP_NAMES:
                continue
            codes = re.findall(r"\d+", m.group(2))
            key = f"{norm(name)}|{codes_key(codes)}"
            if key in seen:
                continue
            seen.add(key)
            items.append({"name": name, "code": " ".join(codes), "imageUrl": lookup(name, codes)})
        looks.append({"title": title, "text": body_clean, "items": items})

    return looks


def parse_colors(raw, model_name):
    out = []
    if not isinstance(raw, str):
        return out
    for part in raw.split(" | "):
        m = re.match(r"^\s*(.+?)\s*\(([\d\s]+)\)\s*:\s*(.*)$", part.strip())
        if not m:
            continue
        name, codes, url = m.group(1).strip(), re.findall(r"\d+", m.group(2)), m.group(3).strip()
        url = enc(url) if url.startswith("http") else None
        resolved = lookup(model_name, codes) or url
        out.append({"name": name, "code": " ".join(codes), "imageUrl": resolved})
    return out


def split_pipe(raw):
    if not isinstance(raw, str):
        return []
    return [clean(p) for p in raw.split("|") if p.strip()]


from test_universal_objections import parse_universal_objections

def parse_objections(raw, lang="ru"):
    return parse_universal_objections(raw, lang)



# ---------------------------------------------------------------- build
df = pd.read_excel(MODELS_XLSX)
name_to_id = {norm(r["Nome Modello"]): int(r["ID"]) for _, r in df.iterrows()}

models = []
for _, r in df.iterrows():
    name = str(r["Nome Modello"]).strip()
    looks = parse_looks(r["Styling / Abbinamenti"], name)
    for lk in looks:
        for it in lk["items"]:
            lid = name_to_id.get(norm(it["name"]))
            if lid and lid != int(r["ID"]):
                it["modelId"] = lid
    models.append(
        {
            "id": int(r["ID"]),
            "name": name,
            "description": {
                "en": clean(r["Descrizione Eng"]) if isinstance(r["Descrizione Eng"], str) else "",
                "ru": clean(r["Descrizione"]) if isinstance(r["Descrizione"], str) else "",
            },
            "colors": parse_colors(r["Colori"], name),
            "looks": looks,
            "advice": {
                "en": split_pipe(r["Consigli di Vendita Eng"]) or split_pipe(r["Consigli di Vendita"]),
                "ru": split_pipe(r["Consigli di Vendita"]),
            },
            "objections": {
                "en": parse_objections(r["Gestione Obiezioni Eng"], "en") or parse_objections(r["Gestione Obiezioni"], "ru"),
                "ru": parse_objections(r["Gestione Obiezioni"], "ru"),
            },

        }
    )

models.sort(key=lambda m: m["name"].lower())

# Second pass: for cited garments absent from the image list, borrow the picture
# from that model's own colour variants (exact colour code first).
by_id = {m["id"]: m for m in models}
recovered = 0
for m in models:
    for lk in m["looks"]:
        for it in lk["items"]:
            if it["imageUrl"]:
                continue
            target = by_id.get(it.get("modelId")) or (m if norm(it["name"]) == norm(m["name"]) else None)
            if not target:
                continue
            wanted = set(it["code"].split())
            pick = next(
                (c["imageUrl"] for c in target["colors"] if c["imageUrl"] and wanted & set(c["code"].split())),
                None,
            ) or next((c["imageUrl"] for c in target["colors"] if c["imageUrl"]), None)
            if pick:
                it["imageUrl"] = pick
                recovered += 1
print(f"recovered_from_variants={recovered}")

import os
import shutil

outdir = "src/data/models"
shutil.rmtree(outdir, ignore_errors=True)
os.makedirs(outdir, exist_ok=True)
for m in models:
    with open(f"{outdir}/{m['id']}.json", "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False)
with open("src/data/index.json", "w", encoding="utf-8") as f:
    json.dump([{"id": m["id"], "name": m["name"]} for m in models], f, ensure_ascii=False)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(models, f, ensure_ascii=False)



cited = sum(len(l["items"]) for m in models for l in m["looks"])
missing = sum(1 for m in models for l in m["looks"] for i in l["items"] if not i["imageUrl"])
colors = sum(len(m["colors"]) for m in models)
no_color_img = sum(1 for m in models for c in m["colors"] if not c["imageUrl"])
print(f"models={len(models)} cited_items={cited} without_image={missing}")
print(f"colors={colors} without_image={no_color_img}")
print("top unmatched:", sorted(unmatched.items(), key=lambda x: -x[1])[:15])
