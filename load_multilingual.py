#!/usr/bin/env python3
"""
Load the multilingual CSV file FW226-Training/226FWCollectionMultilingua.csv
and provide access to translations in 9 languages:
Russian (base), English, Arabic, Georgian, Armenian, Latvian,
Lithuanian, Polish, Ukrainian.

Special rules:
- For field "Styling / Abbinamenti":
    * Russian version -> use base column (Russian Styling)
    * All other languages -> use English column (Styling / Abbinamenti Eng)
- For field "Gestione Obiezioni":
    * Always use base column (original Russian column), regardless of target language.

Usage:
    python load_multilingual.py <csv_file>
"""

import csv
import sys
from typing import List, Dict, Any

def load_multilingual_csv(filepath: str) -> List[Dict[str, Any]]:
    """
    Load the CSV file with semicolon delimiter and quotechar double quote.
    Handles UTF-8 BOM if present.
    Returns a list of dictionaries, each representing a row.
    """
    with open(filepath, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';', quotechar='"')
        # Clean fieldnames: remove surrounding quotes
        reader.fieldnames = [name.strip('"') for name in reader.fieldnames]
        rows = []
        for row in reader:
            # Strip quotes from values if they are strings
            cleaned = {k: v.strip('"') if isinstance(v, str) else v for k, v in row.items()}
            rows.append(cleaned)
        return rows

# Language to suffix mapping (empty string for Russian/base)
LANG_SUFFIX = {
    'Russian': '',
    'English': 'Eng',
    'Arabic': 'Ara',
    'Georgian': 'Geo',
    'Armenian': 'Arm',
    'Latvian': 'Let',
    'Lithuanian': 'Lit',
    'Polish': 'Pol',
    'Ukrainian': 'Ukr',
}

def get_field_value(row: Dict[str, Any], field: str, language: str) -> str:
    """
    Return the value for `field` in the given `language` according to the special rules.
    If the language-specific value is empty, fall back to English (for non-Russian, non-English languages)
    or to the base (Russian) column.
    """
    if language not in LANG_SUFFIX:
        raise ValueError(f'Unsupported language: {language}')
    
    # Special handling for Styling / Abbinamenti
    if field == 'Styling / Abbinamenti':
        if language == 'Russian':
            col = field  # base column (Russian)
        else:
            col = f'{field} Eng'  # English column
        val = row.get(col, '')
        # If empty, fallback to base column (Russian)
        if not val.strip():
            val = row.get(field, '')
        return val
    
    # Special handling for Gestione Obiezioni: always use base column (original)
    if field == 'Gestione Obiezioni':
        val = row.get(field, '')
        return val
    
    # For all other fields: try language-specific column, fallback to English if empty,
    # then fallback to base (Russian) if English is also empty
    suffix = LANG_SUFFIX[language]
    if suffix == '':
        # Russian: use base column
        col = field
        val = row.get(col, '')
        if not val.strip():
            # Fallback to English if available
            val = row.get(f'{field} Eng', '')
        if not val.strip():
            # Final fallback to base (Russian) - already have it, but just in case
            val = row.get(field, '')
        return val
    else:
        # Non-Russian, non-English language: use language-specific column
        col = f'{field} {suffix}'
        val = row.get(col, '')
        if not val.strip():
            # Fallback to English, not Russian
            val = row.get(f'{field} Eng', '')
        if not val.strip():
            # Final fallback to base (Russian)
            val = row.get(field, '')
        return val

def list_language_columns(fieldnames: List[str]) -> Dict[str, List[str]]:
    """
    Given the CSV fieldnames, return a dict mapping language to the actual
    column names present in the CSV.
    """
    lang_cols = {lang: [] for lang in LANG_SUFFIX}
    for field in fieldnames:
        # Determine language of this column
        matched = False
        for lang, suffix in LANG_SUFFIX.items():
            if suffix == '':
                # Base column: no suffix
                if not any(field.endswith(f' {suf}') for suf in LANG_SUFFIX.values() if suf):
                    lang_cols[lang].append(field)
                    matched = True
                    break
            else:
                if field.endswith(f' {suffix}'):
                    lang_cols[lang].append(field)
                    matched = True
                    break
        if not matched:
            # Should not happen, but fallback to Russian
            lang_cols['Russian'].append(field)
    return lang_cols

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <csv_file>")
        sys.exit(1)
    csv_file = sys.argv[1]
    rows = load_multilingual_csv(csv_file)
    if not rows:
        print("No rows loaded.")
        return
    fieldnames = list(rows[0].keys())
    lang_cols = list_language_columns(fieldnames)
    print(f"Loaded {len(rows)} rows from {csv_file}")
    print("\nLanguage columns detected:")
    for lang, cols in lang_cols.items():
        if cols:
            print(f"  {lang}: {len(cols)} columns -> {', '.join(cols[:3])}{'...' if len(cols) > 3 else ''}")
    # Demonstrate: show first row's selected fields in each language
    print("\nExample from first row:")
    sample_language = ['Russian', 'English', 'Arabic', 'Georgian', 'Armenian', 'Latvian', 'Lithuanian', 'Polish', 'Ukrainian']
    for lang in sample_language:
        descr = get_field_value(rows[0], 'Descrizione', lang)
        styling = get_field_value(rows[0], 'Styling / Abbinamenti', lang)
        objections = get_field_value(rows[0], 'Gestione Obiezioni', lang)
        print(f"\n{lang}:")
        print(f"  Descrizione: {descr[:80]}{'...' if len(descr) > 80 else ''}")
        print(f"  Styling / Abbinamenti: {styling[:80]}{'...' if len(styling) > 80 else ''}")
        print(f"  Gestione Obiezioni: {objections[:80]}{'...' if len(objections) > 80 else ''}")

if __name__ == '__main__':
    main()