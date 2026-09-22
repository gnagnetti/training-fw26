#!/usr/bin/env python3
import csv
import re

def clean_text(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""
    t = text
    t = re.sub(r"\.?\s*!\[([^\]]*)\]\([^)]+\)\s*\{[^}]*\}", "", t)
    t = re.sub(r"!\[([^\]]*)\]\([^)]*\)", "", t)
    t = re.sub(r"https?://\S+", "", t)
    t = re.sub(r"\([^)]*nan[^)]*\)", "", t, flags=re.I)
    t = re.sub(r"\s+([,.;:!?،؛])", r"\1", t)
    t = re.sub(r"([,.;:!?،؛])\s*([,.;:!?،؛])+", r"\1", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip(" \t\n\r,;«»“”\"':،؛")

def parse_advice(raw_text: str) -> list[str]:
    if not raw_text or not isinstance(raw_text, str):
        return []
    cleaned = clean_text(raw_text)
    if not cleaned:
        return []
    
    if "|" in cleaned:
        parts = [clean_text(p) for p in cleaned.split("|") if clean_text(p)]
        if parts:
            return parts
            
    if re.search(r"(?:^|\s+)-\s+", cleaned):
        parts = re.split(r"(?:^|\s+)-\s+", cleaned)
        out = [clean_text(p) for p in parts if clean_text(p)]
        if out:
            return out

    if "\n" in cleaned:
        parts = [clean_text(p) for p in cleaned.split("\n") if clean_text(p)]
        if parts:
            return parts

    return [cleaned]

def test():
    with open('226FWCollectionMultilingua.csv', mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        rows = list(reader)

    langs = {
        'ru': 'Consigli di Vendita',
        'en': 'Consigli di Vendita Eng',
        'ar': 'Consigli di Vendita Ara',
        'ka': 'Consigli di Vendita Geo',
        'hy': 'Consigli di Vendita Arm',
        'lv': 'Consigli di Vendita Let',
        'lt': 'Consigli di Vendita Lit',
        'pl': 'Consigli di Vendita Pol',
        'uk': 'Consigli di Vendita Ukr',
    }

    for lang, col in langs.items():
        total_items = 0
        non_empty = 0
        for r in rows:
            raw = r.get(col, '')
            adv = parse_advice(raw)
            if adv:
                non_empty += 1
                total_items += len(adv)
        print(f"[{lang.upper()}] Models with advice: {non_empty}/273, Total advice items: {total_items}, Avg per model: {total_items/max(1, non_empty):.1f}")

    print("\n--- SAMPLE FOR GESSICA (ID 402) ---")
    gessica = [r for r in rows if r['ID'] == '402'][0]
    for lang, col in langs.items():
        adv = parse_advice(gessica.get(col, ''))
        print(f"[{lang.upper()} ({len(adv)} items)]:")
        for idx, item in enumerate(adv, 1):
            print(f"   {idx}. {item[:80]}...")

if __name__ == '__main__':
    test()
