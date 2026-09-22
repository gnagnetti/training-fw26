#!/usr/bin/env python3
import glob
import json
import os
import re

def main():
    models = glob.glob('src/data/models/*.json')
    print(f"Total JSON models: {len(models)}")
    
    languages = ['en', 'ru', 'ar', 'hy', 'ka', 'uk', 'lv', 'lt', 'pl']
    
    for lang in languages:
        total = 0
        has_objs = 0
        single_empty_q = 0
        multiple_items = 0
        clean_items = 0
        
        sample_unparsed = []
        
        for m_path in models:
            with open(m_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            total += 1
            objs = data.get('objections', {}).get(lang, [])
            if not objs:
                continue
            has_objs += 1
            if len(objs) == 1 and not objs[0].get('q', '').strip():
                single_empty_q += 1
                if len(sample_unparsed) < 3:
                    sample_unparsed.append((data.get('id'), data.get('name'), objs[0].get('a', '')[:100]))
            elif len(objs) > 1:
                multiple_items += 1
                if all(o.get('q', '').strip() and o.get('a', '').strip() for o in objs):
                    clean_items += 1
                    
        print(f"[{lang}] Total={total}, HasObjs={has_objs}, SingleEmptyQ={single_empty_q}, MultipleItems={multiple_items}, CleanItems={clean_items}")
        if sample_unparsed:
            for s in sample_unparsed:
                print(f"   Sample unparsed ID {s[0]} ({s[1]}): {repr(s[2])}")

if __name__ == '__main__':
    main()
