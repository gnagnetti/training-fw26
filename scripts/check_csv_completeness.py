#!/usr/bin/env python3
import csv

def check_csv_completeness():
    with open('226FWCollectionMultilingua.csv', mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        rows = list(reader)

    print(f"Total rows in CSV: {len(rows)}")

    langs = {
        'ru': ('Descrizione', 'Consigli di Vendita', 'Gestione Obiezioni'),
        'en': ('Descrizione Eng', 'Consigli di Vendita Eng', 'Gestione Obiezioni Eng'),
        'ar': ('Descrizione Ara', 'Consigli di Vendita Ara', 'Gestione Obiezioni Ara'),
        'ka': ('Descrizione Geo', 'Consigli di Vendita Geo', 'Gestione Obiezioni Geo'),
        'hy': ('Descrizione Arm', 'Consigli di Vendita Arm', 'Gestione Obiezioni Arm'),
        'lv': ('Descrizione Let', 'Consigli di Vendita Let', 'Gestione Obiezioni Let'),
        'lt': ('Descrizione Lit', 'Consigli di Vendita Lit', 'Gestione Obiezioni Lit'),
        'pl': ('Descrizione Pol', 'Consigli di Vendita Pol', 'Gestione Obiezioni Pol'),
        'uk': ('Descrizione Ukr', 'Consigli di Vendita Ukr', 'Gestione Obiezioni Ukr'),
    }

    for lang, (desc_col, adv_col, obj_col) in langs.items():
        desc_count = sum(1 for r in rows if r.get(desc_col, '').strip())
        adv_count = sum(1 for r in rows if r.get(adv_col, '').strip())
        obj_count = sum(1 for r in rows if r.get(obj_col, '').strip())
        print(f"[{lang.upper()}] Desc: {desc_count}/{len(rows)}, Advice: {adv_count}/{len(rows)}, Objections: {obj_count}/{len(rows)}")

if __name__ == '__main__':
    check_csv_completeness()
