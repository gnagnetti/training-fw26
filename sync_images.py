import csv
import difflib
import json
import os
import re
import sys

def normalize_text(text: str) -> str:
    """Normalizza testo rimuovendo spazi multipli e caratteri speciali."""
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text.strip())
    return text.lower()

class ImageDatabase:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.exact_map = {}       # (norm_model, norm_color) -> url
        self.color_to_models = {} # norm_color -> list of (norm_model, orig_model, url)
        self.raw_entries = []
        self.load_csv()

    def load_csv(self):
        if not os.path.exists(self.csv_path):
            print(f"[ERRORE] File non trovato: {self.csv_path}")
            sys.exit(1)

        with open(self.csv_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.reader(f, delimiter=";")
            for row in reader:
                if not row or len(row) < 2:
                    continue
                modello_colore = row[0].strip()
                url = row[1].strip()

                if not url or modello_colore.lower() == "modellocolore":
                    continue

                # Estrazione nome modello e colore: es. "Caprese       B (0101)" -> "Caprese B", "0101"
                match = re.match(r"^(.*?)\s*\((.*?)\)$", modello_colore)
                if match:
                    model_name = match.group(1).strip()
                    color_code = match.group(2).strip()
                else:
                    parts = modello_colore.rsplit(" ", 1)
                    model_name = parts[0].strip()
                    color_code = parts[1].strip() if len(parts) > 1 else ""

                norm_model = normalize_text(model_name)
                norm_color = normalize_text(color_code)

                self.exact_map[(norm_model, norm_color)] = url
                
                if norm_color not in self.color_to_models:
                    self.color_to_models[norm_color] = []
                self.color_to_models[norm_color].append((norm_model, model_name, url))
                self.raw_entries.append((model_name, color_code, url))

        print(f"[OK] Caricate {len(self.exact_map)} associazioni da {self.csv_path}")

    def find_image(self, model: str, color: str, threshold: float = 0.75):
        """
        Cerca l'URL dell'immagine con fallback fuzzy per gestire refusi
        (es. Sigle vs Single, Cips vs Clips).
        """
        norm_m = normalize_text(model)
        norm_c = normalize_text(color)

        # 1. Match Esatto normalizzato
        if (norm_m, norm_c) in self.exact_map:
            return self.exact_map[(norm_m, norm_c)], "ESATTO", model

        # 2. Match Fuzzy sullo stesso codice colore (molto affidabile)
        if norm_c in self.color_to_models:
            candidates = self.color_to_models[norm_c]
            best_ratio = 0.0
            best_match = None

            for c_norm_m, orig_m, url in candidates:
                ratio = difflib.SequenceMatcher(None, norm_m, c_norm_m).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = (url, orig_m)

            if best_ratio >= threshold:
                return best_match[0], f"FUZZY ({best_ratio:.2f})", best_match[1]

        # 3. Match Fuzzy Globale
        all_keys = list(self.exact_map.keys())
        model_keys = [k[0] for k in all_keys if k[1] == norm_c]
        if model_keys:
            closest = difflib.get_close_matches(norm_m, model_keys, n=1, cutoff=threshold)
            if closest:
                return self.exact_map[(closest[0], norm_c)], "FUZZY-GLOBALE", closest[0]

        return None, "NON TROVATO", None

    def export_json_map(self, output_file: str = "images_map.json"):
        """Esporta un file JSON pronto per essere importato nel Worker Cloudflare."""
        export_data = {}
        for (m, c), url in self.exact_map.items():
            key = f"{m}_{c}".replace(" ", "_")
            export_data[key] = url

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        print(f"[OK] Esportata mappa immagini in: {output_file}")

    def patch_json_files(self, directory: str):
        """Scansiona e aggiorna automaticamente i file JSON nel repository."""
        count_updated = 0
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".json") and file != "images_map.json" and not file.startswith("package"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            data = json.load(f)

                        updated = self._recursive_update(data)
                        if updated:
                            with open(path, "w", encoding="utf-8") as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                            print(f"[AGGIORNATO] {path}")
                            count_updated += 1
                    except Exception as e:
                        pass
        print(f"[COMPLETATO] Aggiornati {count_updated} file JSON.")

    def _recursive_update(self, node):
        updated = False
        if isinstance(node, dict):
            # Se il dizionario contiene nome modello e colore
            model = node.get("modello") or node.get("model") or node.get("name") or node.get("nome")
            color = node.get("colore") or node.get("color") or node.get("codiceColore")

            if model and color:
                url, status, matched_name = self.find_image(str(model), str(color))
                if url:
                    for key in ["image", "img", "foto", "url", "imageUrl", "Style Image URL_1"]:
                        if key in node and (not node[key] or "Нет изображения" in str(node[key]) or node[key] != url):
                            node[key] = url
                            updated = True
                            break

            for v in node.values():
                if self._recursive_update(v):
                    updated = True

        elif isinstance(node, list):
            for item in node:
                if self._recursive_update(item):
                    updated = True
        return updated


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Trova e sincronizza immagini da url.csv")
    parser.add_argument("--csv", default="url.csv", help="Percorso di url.csv")
    parser.add_argument("--search", nargs=2, metavar=("MODELLO", "COLORE"), help="Cerca un singolo articolo: es. --search 'Single' '2731 1167'")
    parser.add_argument("--export", action="store_true", help="Esporta images_map.json per il worker")
    parser.add_argument("--patch-repo", metavar="DIR", help="Aggiorna ricorsivamente i file JSON nella cartella specificata")

    args = parser.parse_args()
    db = ImageDatabase(args.csv)

    if args.search:
        m, c = args.search
        url, match_type, matched_with = db.find_image(m, c)
        print(f"\nRicerca per: Modello='{m}', Colore='{c}'")
        if url:
            print(f"-> Trovato ({match_type}, match con '{matched_with}'):")
            print(f"   {url}")
        else:
            print("-> Nessuna immagine corrispondente trovata in url.csv.")

    elif args.patch_repo:
        db.patch_json_files(args.patch_repo)

    elif args.export:
        db.export_json_map()

    else:
        # Test automatico sugli articoli problematici della schermata
        test_items = [
            ("Single", "2731 1167"),
            ("Clips", "1161"),
            ("Contagiri", "0202"),
            ("Bacche", "0201"),
            ("Manos F", "0101"),
            ("Rivolo", "3278"),
            ("Casistica", "0101 2352")
        ]
        print("\n--- TEST ARTICOLI DELLA SCHERMATA ---")
        for m, c in test_items:
            url, status, orig = db.find_image(m, c)
            status_desc = f"TROVATO tramite {status} ('{orig}')" if url else "NON PRESENTE IN CSV"
            print(f"• {m:<12} {c:<12} -> {status_desc}")
            if url:
                print(f"  {url}")sync_images.py
