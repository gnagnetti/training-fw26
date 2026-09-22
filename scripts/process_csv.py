#!/usr/bin/env python3
"""
Transform fashion model CSV into optimized multilingual JSON structure.

Input: CSV con colonne piatte per ogni lingua
Columns: ID, Nome Modello, Descrizione, Descrizione Eng, Descrizione Ar, 
          Colori, Styling / Abbinamenti, Styling / Abbinamenti Eng,
          Consigli di Vendita*, Gestione Obiezioni*

Output: src/data/models.json with dynamic language support

Language Mapping:
- RU: Descrizione (no suffix) + Styling / Abbinamenti (no suffix)
- EN: Descrizione Eng + Styling / Abbinamenti Eng
- AR: Descrizione Ar + Consigli di Vendita Ara + Gestione Obiezioni Ara
- GEO: Descrizione Geo + Consigli di Vendita Geo + Gestione Obiezioni Geo
- ARM: Descrizione Arm + Consigli di Vendita Arm + Gestione Obiezioni Arm
- LET: Descrizione Let + Consigli di Vendita Let + Gestione Obiezioni Let
- LIT: Descrizione Lit + Consigli di Vendita Lit + Gestione Obiezioni Lit
- POL: Descrizione Pol + Consigli di Vendita Pol + Gestione Obiezioni Pol
- UKR: Descrizione Ukr + Consigli di Vendita Ukr + Gestione Obiezioni Ukr
"""

import pandas as pd
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


# Language codes mapping
LANGUAGE_MAP = {
    'RU': {'suffix': '', 'name': 'Russo'},
    'EN': {'suffix': ' Eng', 'name': 'Inglese'},
    'AR': {'suffix': ' Ara', 'name': 'Arabo'},
    'GEO': {'suffix': ' Geo', 'name': 'Georgiano'},
    'ARM': {'suffix': ' Arm', 'name': 'Armeno'},
    'LET': {'suffix': ' Let', 'name': 'Lettone'},
    'LIT': {'suffix': ' Lit', 'name': 'Lituano'},
    'POL': {'suffix': ' Pol', 'name': 'Polacco'},
    'UKR': {'suffix': ' Ukr', 'name': 'Ucraino'},
}


def clean_text(text: Optional[str]) -> str:
    """Clean and normalize text values."""
    if pd.isna(text) or text is None:
        return ""
    text = str(text).strip()
    return text if text else ""


def parse_colors(color_string: str) -> List[Dict[str, Any]]:
    """
    Parse the Colori column into color variants.
    
    Expected format variations:
    - "0101 Bianco, 2449 Nero, 0303 Grigio"
    - "0101, 2449, 0303"
    
    Returns list of {code, name, imageUrl}
    """
    if not color_string:
        return []
    
    color_variants = []
    # Split by comma or semicolon
    parts = re.split(r'[,;]', color_string)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Try to extract code and name
        # Pattern: "XXXX Name" or just "XXXX"
        match = re.match(r'(\d{4})\s*(.*)', part)
        if match:
            code = match.group(1)
            name = clean_text(match.group(2)) or code
            color_variants.append({
                'code': code,
                'name': name,
                'imageUrl': None  # Will be populated if images exist
            })
    
    return color_variants


def process_csv(csv_path: str, output_path: str, delimiter: str = '\t') -> None:
    """
    Transform flat CSV into optimized multilingual JSON structure.
    
    Args:
        csv_path: Path to input CSV
        output_path: Path to write models.json
        delimiter: CSV delimiter (tab by default for TSV format)
    """
    
    # Read CSV with tab delimiter by default
    df = pd.read_csv(csv_path, delimiter=delimiter, encoding='utf-8')
    
    print(f"📖 Loaded {len(df)} rows from {csv_path}")
    print(f"📋 Columns: {list(df.columns)}")
    
    models = []
    
    # Process each row
    for idx, row in df.iterrows():
        try:
            model_id = int(row.get('ID', 0))
            model_name = clean_text(row.get('Nome Modello', ''))
            colori_text = clean_text(row.get('Colori', ''))
            
            # Validate required fields
            if not model_id or not model_name:
                print(f"⚠️  Skipping row {idx}: missing ID or Nome Modello")
                continue
            
            # Build multilingual content dictionaries
            descriptions = {}
            styling_abbinamenti = {}
            consigli_vendita = {}
            gestione_obiezioni = {}
            
            # Extract content for each language
            for lang_code, lang_info in LANGUAGE_MAP.items():
                suffix = lang_info['suffix']
                
                # Descriptions
                desc_col = f'Descrizione{suffix}'
                if desc_col in df.columns:
                    descriptions[lang_code] = clean_text(row.get(desc_col, ''))
                
                # Styling/Abbinamenti - only from Russian (no suffix) and English
                if lang_code == 'RU':
                    styling_col = 'Styling / Abbinamenti'
                elif lang_code == 'EN':
                    styling_col = 'Styling / Abbinamenti Eng'
                else:
                    # For other languages, use English as fallback
                    styling_col = 'Styling / Abbinamenti Eng'
                
                if styling_col in df.columns:
                    styling_abbinamenti[lang_code] = clean_text(row.get(styling_col, ''))
                
                # Consigli di Vendita
                consigli_col = f'Consigli di Vendita{suffix}'
                if consigli_col in df.columns:
                    consigli_vendita[lang_code] = clean_text(row.get(consigli_col, ''))
                
                # Gestione Obiezioni
                gestione_col = f'Gestione Obiezioni{suffix}'
                if gestione_col in df.columns:
                    gestione_obiezioni[lang_code] = clean_text(row.get(gestione_col, ''))
            
            # Parse color variants
            color_variants = parse_colors(colori_text)
            
            # Create model object
            model = {
                'id': model_id,
                'name': model_name,
                'descriptions': descriptions,
                'stylingAdvice': styling_abbinamenti,
                'salesAdvice': consigli_vendita,
                'objectionHandling': gestione_obiezioni,
                'colorVariants': color_variants
            }
            
            models.append(model)
        
        except Exception as e:
            print(f"❌ Error processing row {idx}: {e}")
            continue
    
    # Get unique languages present in data
    all_languages = set(LANGUAGE_MAP.keys())
    present_languages = []
    for lang in ['RU', 'EN', 'AR', 'GEO', 'ARM', 'LET', 'LIT', 'POL', 'UKR']:
        if lang in all_languages:
            present_languages.append(lang)
    
    # Create output structure
    output_data = {
        'languages': present_languages,
        'models': models
    }
    
    # Write JSON
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Successfully processed and wrote to {output_path}")
    print(f"   Languages: {present_languages}")
    print(f"   Models: {len(models)}")
    print(f"   Total color variants: {sum(len(m['colorVariants']) for m in models)}")


if __name__ == "__main__":
    import sys
    
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "fashion_models.csv"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "src/data/models.json"
    delimiter = sys.argv[3] if len(sys.argv) > 3 else '\t'  # Default to tab
    
    process_csv(csv_path, output_path, delimiter)
