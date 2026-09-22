#!/usr/bin/env python3
"""
Builds clean, parsed objections for all models across all 9 languages without relying on external APIs.
Uses 226FWCollectionMultilingua.csv and existing data.
"""

import csv
import glob
import json
import os
import re

from test_universal_objections import parse_universal_objections, clean_objection_text

ALL_LANGS = ["en", "ru", "pl", "uk", "ar", "hy", "ka", "lv", "lt"]

CSV_LANG_MAP = {
    "ru": "Gestione Obiezioni",
    "en": "Gestione Obiezioni Eng",
    "ar": "Gestione Obiezioni Ara",
    "ka": "Gestione Obiezioni Geo",
    "hy": "Gestione Obiezioni Arm",
    "lv": "Gestione Obiezioni Let",
    "lt": "Gestione Obiezioni Lit",
    "pl": "Gestione Obiezioni Pol",
    "uk": "Gestione Obiezioni Ukr",
}


def clean_str(s: str) -> str:
    if not s:
        return ""
    t = s.strip(" \t\n\r,;«»“”\"':")
    t = re.sub(r"^(?:Objection\s*\d*\s*[:\-]|Response\s*[:\-]|Возражение\s*[:\-]|Ответ\s*[:\-])\s*", "", t, flags=re.I)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip(" \t\n\r,;«»“”\"':")


def load_csv_data():
    csv_by_id = {}
    with open("226FWCollectionMultilingua.csv", mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            m_id = row.get("ID")
            if m_id:
                try:
                    csv_by_id[int(m_id)] = row
                except ValueError:
                    pass
    return csv_by_id


def sanitize_items(items):
    out = []
    if not items:
        return out
    for o in items:
        q = clean_str(o.get("q", ""))
        a = clean_str(o.get("a", ""))
        if not q and not a:
            continue
        # If q is empty but a has Objection: ... Response: ... format, parse it
        if not q and a:
            sub = parse_universal_objections(a, "en") or parse_universal_objections(a, "ru")
            if sub and len(sub) > 0 and all(s.get("q", "").strip() for s in sub):
                for s in sub:
                    sq = clean_str(s.get("q", ""))
                    sa = clean_str(s.get("a", ""))
                    if sq and sa:
                        if not sa.endswith((".", "!", "?", "…")):
                            sa += "."
                        out.append({"q": sq, "a": sa})
                continue
        if q and a:
            if not a.endswith((".", "!", "?", "…")):
                a += "."
            out.append({"q": q, "a": a})
    return out


def main():
    csv_data = load_csv_data()
    model_files = sorted(glob.glob("src/data/models/*.json"), key=lambda x: int(os.path.basename(x).split(".")[0]))
    print(f"Loaded {len(model_files)} model files and {len(csv_data)} CSV rows.")

    updated_count = 0
    all_models = []

    for filepath in model_files:
        with open(filepath, "r", encoding="utf-8") as f:
            model = json.load(f)

        m_id = model["id"]
        csv_row = csv_data.get(m_id, {})
        existing_objs = model.get("objections", {})

        final_objections = {}

        for lang in ALL_LANGS:
            col = CSV_LANG_MAP.get(lang)
            raw_csv = csv_row.get(col, "") if col else ""
            parsed_from_csv = parse_universal_objections(raw_csv, lang)
            sanitized_csv = sanitize_items(parsed_from_csv)

            # Check existing json
            existing_lang_items = existing_objs.get(lang, [])
            sanitized_existing = sanitize_items(existing_lang_items)

            if len(sanitized_csv) >= len(sanitized_existing) and len(sanitized_csv) > 0:
                final_objections[lang] = sanitized_csv
            elif len(sanitized_existing) > 0:
                final_objections[lang] = sanitized_existing
            else:
                final_objections[lang] = []

        model["objections"] = final_objections

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(model, f, ensure_ascii=False, indent=2)

        all_models.append(model)
        updated_count += 1

    # Update src/data/models.json
    with open("src/data/models.json", "w", encoding="utf-8") as f:
        json.dump(all_models, f, ensure_ascii=False)

    # Update src/locales/*.json
    os.makedirs("src/locales", exist_ok=True)
    for lang in ALL_LANGS:
        locale_data = {
            "lang": lang,
            "models": {}
        }
        for m in all_models:
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
                "objections": obj
            }

        with open(f"src/locales/{lang}.json", "w", encoding="utf-8") as f:
            json.dump(locale_data, f, ensure_ascii=False, indent=2)

    print(f"Updated all {updated_count} models in src/data/models/*.json, models.json, and locales/*.json")


if __name__ == "__main__":
    main()
