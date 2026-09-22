#!/usr/bin/env python3
"""
Updates ONLY Arabic objections across all models without modifying any other language.
"""

import csv
import glob
import json
import os
import re

from test_ar_parser import parse_arabic_objections

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


def main():
    csv_data = load_csv_data()
    model_files = sorted(glob.glob("src/data/models/*.json"), key=lambda x: int(os.path.basename(x).split(".")[0]))
    print(f"Loaded {len(model_files)} model files.")

    all_models = []
    updated_count = 0

    for filepath in model_files:
        with open(filepath, "r", encoding="utf-8") as f:
            model = json.load(f)

        m_id = model["id"]
        csv_row = csv_data.get(m_id, {})
        
        raw_ar = csv_row.get("Gestione Obiezioni Ara", "").strip()
        parsed_ar = parse_arabic_objections(raw_ar)

        # Update ONLY model["objections"]["ar"]
        if "objections" not in model:
            model["objections"] = {}

        model["objections"]["ar"] = parsed_ar if parsed_ar else []

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(model, f, ensure_ascii=False, indent=2)

        all_models.append(model)
        if parsed_ar:
            updated_count += 1

    # Update src/data/models.json
    with open("src/data/models.json", "w", encoding="utf-8") as f:
        json.dump(all_models, f, ensure_ascii=False)

    # Update ONLY src/locales/ar.json
    os.makedirs("src/locales", exist_ok=True)
    locale_data = {
        "lang": "ar",
        "models": {}
    }
    for m in all_models:
        m_id = str(m["id"])
        desc = m.get("description", {}).get("ar") or m.get("description", {}).get("en") or ""
        adv = m.get("advice", {}).get("ar") or m.get("advice", {}).get("en") or []
        obj = m.get("objections", {}).get("ar") or []
        lks = []
        for lk in m.get("looks", []):
            t_title = None
            if lk.get("title"):
                if isinstance(lk["title"], dict):
                    t_title = lk["title"].get("ar") or lk["title"].get("en")
                else:
                    t_title = lk["title"]
            t_text = ""
            if lk.get("text"):
                if isinstance(lk["text"], dict):
                    t_text = lk["text"].get("ar") or lk["text"].get("en") or ""
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

    with open("src/locales/ar.json", "w", encoding="utf-8") as f:
        json.dump(locale_data, f, ensure_ascii=False, indent=2)

    print(f"Updated Arabic objections for {updated_count} models in src/data/models/*.json, models.json, and locales/ar.json.")


if __name__ == "__main__":
    main()
