#!/usr/bin/env python3
import csv
import re

def inspect_advice():
    with open('226FWCollectionMultilingua.csv', mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        rows = list(reader)

    advice_cols = {
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

    for lang, col in advice_cols.items():
        print(f"=== {lang.upper()} ({col}) ===")
        has_pipe = 0
        has_dash = 0
        single_block = 0
        empty = 0
        for r in rows:
            txt = r.get(col, '').strip()
            if not txt:
                empty += 1
            elif '|' in txt:
                has_pipe += 1
            elif re.search(r'(?:^|\s+)-\s+', txt):
                has_dash += 1
            else:
                single_block += 1
        print(f"Total: {len(rows)}, Has Pipe: {has_pipe}, Has Dash: {has_dash}, Single block: {single_block}, Empty: {empty}")

if __name__ == '__main__':
    inspect_advice()
