#!/usr/bin/env python3
"""
Translates all models' dynamic content into all supported languages:
en, ru, pl, ar, hy, ka, uk, lv, lt.

Rules:
- Keep model proper names (Casilda, Cuoricino, Osten E, Fenice B, etc.)
- Keep codes and numbers (ID #383, 0838 0202, 2026/2027, etc.)
- Translate product descriptions, lookbook texts & titles, sales advice, objections.
- Export localization files to src/locales/*.json
"""

import glob
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

TARGET_LANGS = ["pl", "uk", "ar", "hy", "ka", "lv", "lt"]
ALL_LANGS = ["en", "ru", "pl", "uk", "ar", "hy", "ka", "lv", "lt"]


def translate_raw(text: str, target: str, source: str = "auto") -> str:
    if not text or not text.strip():
        return text
    # Fix Italian terms transcribed in Russian
    t = text.replace("кабаном", "caban").replace("кабан", "caban")
    url = "https://translate.googleapis.com/translate_a/single?" + urllib.parse.urlencode({
        "client": "gtx",
        "sl": source,
        "tl": target,
        "dt": "t",
        "q": t,
    })
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=18) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return "".join([part[0] for part in data[0] if part[0]])
        except Exception as err:
            time.sleep(1.0 + attempt * 1.5)
            if attempt == 2:
                print(f"Translate error for {target} on text '{text[:30]}': {err}")
                return text
    return text


def translate_bundle(texts: list[str], target: str, source: str = "auto") -> list[str]:
    if not texts:
        return []
    sep = "\n<<<SEP>>>\n"
    prepared = [t.replace("кабаном", "caban") if t and t.strip() else "---EMPTY---" for t in texts]
    joined = sep.join(prepared)
    translated_full = translate_raw(joined, target, source)
    parts = translated_full.split("<<<SEP>>>")
    out = []
    for i, p in enumerate(parts):
        cleaned = p.strip()
        if cleaned == "---EMPTY---" or (i < len(texts) and not texts[i].strip()):
            out.append("")
        else:
            out.append(cleaned)
    while len(out) < len(texts):
        out.append(texts[len(out)])
    return out[:len(texts)]


def is_already_processed(model: dict) -> bool:
    desc = model.get("description", {})
    if not all(lang in desc for lang in TARGET_LANGS):
        return False
    looks = model.get("looks", [])
    for lk in looks:
        txt = lk.get("text")
        if not isinstance(txt, dict) or not all(lang in txt for lang in TARGET_LANGS):
            return False
    advice = model.get("advice", {})
    if not all(lang in advice for lang in TARGET_LANGS):
        return False
    objections = model.get("objections", {})
    if not all(lang in objections for lang in TARGET_LANGS):
        return False
    return True


def process_model(model_path: str, force: bool = False) -> dict:
    with open(model_path, "r", encoding="utf-8") as f:
        model = json.load(f)

    if not force and is_already_processed(model):
        return model

    # 1. DESCRIPTION
    desc = model.get("description", {})
    source_desc = desc.get("en") or desc.get("ru") or ""
    desc_source_lang = "en" if desc.get("en") else "ru"

    # 2. LOOKS
    looks = model.get("looks", [])
    look_texts = []
    look_titles = []
    for lk in looks:
        txt = lk.get("text")
        if isinstance(txt, dict):
            txt = txt.get("ru") or txt.get("en") or ""
        look_texts.append(txt or "")

        ttl = lk.get("title")
        if isinstance(ttl, dict):
            ttl = ttl.get("ru") or ttl.get("en") or ""
        look_titles.append(ttl or "")

    # 3. ADVICE
    advice = model.get("advice", {})
    adv_list = advice.get("en") or advice.get("ru") or []
    adv_source_lang = "en" if advice.get("en") else "ru"

    # 4. OBJECTIONS
    objections = model.get("objections", {})
    obj_list = objections.get("en") or objections.get("ru") or []
    obj_source_lang = "en" if objections.get("en") else "ru"
    obj_qs = [o.get("q", "") for o in obj_list]
    obj_as = [o.get("a", "") for o in obj_list]

    # Translate looks to English first if original looks were Russian
    looks_in_en = {}
    if look_texts:
        looks_in_en["texts"] = translate_bundle(look_texts, "en", "ru")
        looks_in_en["titles"] = translate_bundle(look_titles, "en", "ru")
    else:
        looks_in_en["texts"] = []
        looks_in_en["titles"] = []

    def translate_for_lang(target_lang: str):
        res = {}
        if source_desc:
            res["desc"] = translate_raw(source_desc, target_lang, desc_source_lang)
        else:
            res["desc"] = ""

        if look_texts:
            res["look_texts"] = translate_bundle(look_texts, target_lang, "ru")
            res["look_titles"] = translate_bundle(look_titles, target_lang, "ru")
        else:
            res["look_texts"] = []
            res["look_titles"] = []

        if adv_list:
            res["advice"] = translate_bundle(adv_list, target_lang, adv_source_lang)
        else:
            res["advice"] = []

        if obj_qs:
            res["obj_qs"] = translate_bundle(obj_qs, target_lang, obj_source_lang)
            res["obj_as"] = translate_bundle(obj_as, target_lang, obj_source_lang)
        else:
            res["obj_qs"] = []
            res["obj_as"] = []

        return target_lang, res

    with ThreadPoolExecutor(max_workers=7) as executor:
        futures = [executor.submit(translate_for_lang, lang) for lang in TARGET_LANGS]
        translations = dict(f.result() for f in futures)

    # Build updated model structure
    for lang, t_data in translations.items():
        desc[lang] = t_data["desc"]
    model["description"] = desc

    for lang, t_data in translations.items():
        advice[lang] = t_data["advice"]
    model["advice"] = advice

    for lang, t_data in translations.items():
        model_objs = []
        for q, a in zip(t_data["obj_qs"], t_data["obj_as"]):
            model_objs.append({"q": q, "a": a})
        objections[lang] = model_objs
    model["objections"] = objections

    updated_looks = []
    for i, lk in enumerate(looks):
        orig_text = look_texts[i]
        text_dict = {
            "ru": orig_text,
            "en": looks_in_en["texts"][i] if i < len(looks_in_en["texts"]) else orig_text,
        }
        for lang, t_data in translations.items():
            if i < len(t_data["look_texts"]):
                text_dict[lang] = t_data["look_texts"][i]
            else:
                text_dict[lang] = orig_text

        orig_title = look_titles[i]
        if orig_title:
            title_dict = {
                "ru": orig_title,
                "en": looks_in_en["titles"][i] if i < len(looks_in_en["titles"]) else orig_title,
            }
            for lang, t_data in translations.items():
                if i < len(t_data["look_titles"]):
                    title_dict[lang] = t_data["look_titles"][i]
                else:
                    title_dict[lang] = orig_title
        else:
            title_dict = None

        updated_looks.append({
            "title": title_dict,
            "text": text_dict,
            "items": lk.get("items", []),
        })
    model["looks"] = updated_looks

    with open(model_path, "w", encoding="utf-8") as f:
        json.dump(model, f, ensure_ascii=False, indent=2)

    return model


def export_locales():
    os.makedirs("src/locales", exist_ok=True)
    all_files = sorted(glob.glob("src/data/models/*.json"))
    models = []
    for p in all_files:
        with open(p, "r", encoding="utf-8") as f:
            models.append(json.load(f))

    # Save models.json as well
    with open("src/data/models.json", "w", encoding="utf-8") as f:
        json.dump(models, f, ensure_ascii=False)

    for lang in ALL_LANGS:
        locale_data = {
            "lang": lang,
            "models": {}
        }
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
                "objections": obj
            }

        with open(f"src/locales/{lang}.json", "w", encoding="utf-8") as f:
            json.dump(locale_data, f, ensure_ascii=False, indent=2)

    print(f"Exported all locales to src/locales/ (*.json) successfully.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--single":
        model_id = sys.argv[2]
        path = f"src/data/models/{model_id}.json"
        print(f"Translating single model {path}...")
        res = process_model(path, force=True)
        export_locales()
        print(f"Done model {model_id} ({res['name']})")
    elif len(sys.argv) > 1 and sys.argv[1] == "--export-only":
        export_locales()
    else:
        all_files = sorted(glob.glob("src/data/models/*.json"))
        print(f"Processing all {len(all_files)} models with parallel worker pool...")
        # Ensure 383 (Casilda) is guaranteed fresh
        process_model("src/data/models/383.json", force=True)
        
        # Now process remaining models
        remaining = [f for f in all_files if f != "src/data/models/383.json"]
        count = 0
        total = len(remaining)
        
        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = {pool.submit(process_model, path): path for path in remaining}
            for fut in as_completed(futures):
                count += 1
                path = futures[fut]
                try:
                    fut.result()
                    if count % 10 == 0 or count == total:
                        print(f"[{count}/{total}] Processed {os.path.basename(path)}")
                except Exception as e:
                    print(f"Error on {path}: {e}")

        export_locales()
        print("All models translated and localization files exported successfully!")
