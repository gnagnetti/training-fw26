from load_multilingual import load_multilingual_csv, get_field_value

# 1️⃣  Carica tutto il CSV una sola volta
rows = load_multilingual_csv('226FWCollectionMultilingua.csv')

# 2️⃣  Funzione di aiuto che restituisce un dizionario con tutti i campi
#     nella lingua richiesta (rispettando la regola sopra)
def get_record_in_language(row_dict, lang):
    """
    Dato un dizionario che rappresenta una riga del CSV e una lingua
    (uno dei valori: 'Russian', 'English', 'Arabic', 'Georgian',
     'Armenian', 'Latvian', 'Lithuanian', 'Polish', 'Ukrainian'),
    restituisce un nuovo dizionario con tutti i campi tradotti
    secondo le regole specificate.
    """
    fields = [
        'ID', 'Nome Modello', 'Descrizione', 'Colori',
        'Styling / Abbinamenti',
        'Consigli di Vendita',
        'Gestione Obiezioni'
    ]
    out = {}
    for f in fields:
        out[f] = get_field_value(row_dict, f, lang)
    return out

# 3️⃣  Esempio: mostra il primo record in arabo
first_row = rows[0]
arabic_record = get_record_in_language(first_row, 'Arabic')
print("=== Arabo ===")
for k, v in arabic_record.items():
    print(f"{k}: {v}")

# 4️⃣  Esempio: mostra il primo record in inglese
english_record = get_record_in_language(first_row, 'English')
print("\n=== Inglese ===")
for k, v in english_record.items():
    print(f"{k}: {v}")

# 5️⃣  Esempio: mostra il primo record in russo
russian_record = get_record_in_language(first_row, 'Russian')
print("\n=== Russo ===")
for k, v in russian_record.items():
    print(f"{k}: {v}")
