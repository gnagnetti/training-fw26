# 🎨 Architettura Multilinguistica - Guida di Implementazione

## 📋 Panoramica Progetto

Hai aggiornato l'applicazione **style-guide-hub** con:
- ✅ Nuova struttura dati relazionale denormalizzata (CSV)
- ✅ Pipeline Python per trasformazione JSON multilingue
- ✅ Sistema di tipi TypeScript flessibile per N lingue
- ✅ Context React dinamico con fallback automatico
- ✅ Suite completa di componenti UI con gestione errori

---

## 🔄 Flusso di Lavoro Completo

### 1️⃣ **Preparazione Dataset**

**Input:** `226Multi_2.csv` (UTF-8, delimitatore `;`)

Colonne richieste:
```
Lingua | ID | Nome Modello | Descrizione | Colore Nome | Colore Codice | 
Colore URL Immagine | Consigli di Vendita | Gestione Obiezioni
```

**Esempio riga:**
```
IT;1;CANDIDO;Capo elegante in cotone;Bianco;0101;https://images.../0101.jpg;Perfetto per estate;Resistente al lavaggio
```

### 2️⃣ **Trasformazione CSV → JSON**

```bash
# Eseguire lo script Python
python scripts/process_csv.py 226Multi_2.csv src/data/models.json

# Output: src/data/models.json
```

**Struttura JSON generata:**
```json
{
  "languages": ["EN", "IT", "RU"],
  "models": [
    {
      "id": 1,
      "name": "CANDIDO",
      "descriptions": {
        "IT": "Capo elegante in cotone",
        "EN": "Elegant cotton garment",
        "RU": "..."
      },
      "salesAdvice": {
        "IT": "Perfetto per estate",
        "EN": "Perfect for summer",
        "RU": "..."
      },
      "objectionHandling": {
        "IT": "Resistente al lavaggio",
        "EN": "Washable",
        "RU": "..."
      },
      "colorVariants": [
        {
          "name": { "IT": "Bianco", "EN": "White", "RU": "..." },
          "code": "0101",
          "imageUrl": "https://images.../0101.jpg"
        }
      ]
    }
  ]
}
```

---

## 📁 Architettura File

```
src/
├── types/
│   └── model.ts                    # 📝 Tipi TypeScript multilinguistici
├── contexts/
│   └── LanguageContext.tsx         # 🌍 Context per lingua e fallback
├── hooks/
│   └── useModels.ts                # 📦 Hook per caricamento dataset
├── components/
│   ├── ModelCard.tsx               # 🎴 Card compatta modello
│   ├── ColorVariantGallery.tsx     # 🎨 Galleria colori con fallback immagini
│   ├── ModelDetail.tsx             # 📖 Dettagli completi modello
│   ├── SalesAdvice.tsx             # 💡 Consigli di vendita
│   ├── ObjectionHandling.tsx       # 🛡️ Gestione obiezioni
│   └── LanguageSwitcher.tsx        # 🌐 Selettore lingua
└── data/
    └── models.json                 # 📊 Dataset JSON generato

scripts/
└── process_csv.py                  # 🐍 Trasformazione CSV
```

---

## 🔌 Come Integrare nel Tuo App

### Step 1: Setup Provider (App.tsx)

```typescript
import { LanguageProvider } from './contexts/LanguageContext';
import { useModels } from './hooks/useModels';

function App() {
  const { models, languages, isLoading, error } = useModels();

  if (isLoading) return <div>Caricamento...</div>;
  if (error) return <div>Errore: {error}</div>;

  return (
    <LanguageProvider 
      availableLanguages={languages}
      defaultLanguage="IT"
      fallbackLanguage="EN"
    >
      {/* Tuo contenuto */}
      <LanguageSwitcher />
      <ModelsList models={models} />
    </LanguageProvider>
  );
}
```

### Step 2: Usare LanguageSwitcher

```typescript
import LanguageSwitcher from './components/LanguageSwitcher';

export default function Header() {
  return (
    <header className="flex justify-between items-center p-4">
      <h1>Style Guide Hub</h1>
      <LanguageSwitcher />
    </header>
  );
}
```

### Step 3: Visualizzare Modelli

**Opzione A - Vista Compatta (ModelCard):**
```typescript
import ModelCard from './components/ModelCard';
import { useModels } from './hooks/useModels';

function ModelsList() {
  const { models } = useModels();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {models.map(model => (
        <ModelCard key={model.id} model={model} />
      ))}
    </div>
  );
}
```

**Opzione B - Vista Dettagliata (ModelDetail):**
```typescript
import ModelDetail from './components/ModelDetail';

function ModelPage({ modelId }: { modelId: number }) {
  const { getModelById } = useModels();
  const model = getModelById(modelId);

  if (!model) return <div>Modello non trovato</div>;

  return <ModelDetail model={model} />;
}
```

---

## 🌍 Gestione Multilingue

### Hook `useLanguage()`

```typescript
import { useLanguage } from './contexts/LanguageContext';

function MyComponent() {
  const { currentLanguage, setCurrentLanguage, availableLanguages, fallbackLanguage } = useLanguage();

  return (
    <div>
      <p>Lingua attuale: {currentLanguage}</p>
      <button onClick={() => setCurrentLanguage('EN')}>Cambia a English</button>
    </div>
  );
}
```

### Hook `useLocalizedContent()`

```typescript
import { useLocalizedContent } from './contexts/LanguageContext';

function Description({ content }: { content: Record<string, string> }) {
  const localizedText = useLocalizedContent(content);
  
  return <p>{localizedText}</p>;
  // Automaticamente seleziona lingua corrente con fallback a EN se non disponibile
}
```

### Utility `getLocalizedContent()`

```typescript
import { getLocalizedContent } from './types/model';

const advice = getLocalizedContent(
  model.salesAdvice,
  'IT',                    // lingua richiesta
  'EN'                     // lingua fallback
);
```

---

## 🎨 Gestione Errori & Fallback

### Immagini Non Disponibili

**ColorVariantGallery automaticamente:**
- ✅ Mostra placeholder champagne (#F4F0EA)
- ✅ Visualizza icona AlertCircle
- ✅ Mantiene visibile il codice colore
- ✅ Gestisce errori di caricamento

### Contenuti Non Tradotti

**Componenti SalesAdvice e ObjectionHandling:**
- ✅ Mostrano messaggio elegante "Contenuto non disponibile in questa lingua"
- ✅ Fallback automatico a lingua di backup (EN)
- ✅ Non rompono l'interfaccia se campo vuoto

---

## 📊 Strutture Dati Chiave

### ColorVariant
```typescript
interface ColorVariant {
  name: Record<SupportedLanguage, string>;  // Nomi tradotti
  code: string;                              // Es. "0101"
  imageUrl: string | null;                   // URL o null
}
```

### FashionModel
```typescript
interface FashionModel {
  id: number;
  name: string;
  descriptions: Record<SupportedLanguage, string>;      // Descrizioni per lingua
  salesAdvice: Record<SupportedLanguage, string>;       // Consigli vendita
  objectionHandling: Record<SupportedLanguage, string>; // Gestione obiezioni
  colorVariants: ColorVariant[];                        // Array varianti
}
```

### ModelsDataset
```typescript
interface ModelsDataset {
  languages: SupportedLanguage[];  // Es. ["EN", "IT", "RU"]
  models: FashionModel[];          // Tutti i modelli
}
```

---

## 🐍 Script Python - Dettagli Tecnici

### `process_csv.py`

**Input Processing:**
- ✅ Legge CSV con delimitatore `;` (semicolon)
- ✅ Encoding UTF-8 obbligatorio
- ✅ Normalizza testo (strip, uppercase per lingue)

**Aggregazione Dati:**
- ✅ Raggruppa per ID modello
- ✅ Crea dizionari multilingue dinamici
- ✅ Deduplica varianti colore per modello
- ✅ Elimina righe con campi mancanti

**Output:**
- ✅ JSON ben formattato (indent=2)
- ✅ Nessun escape ASCII (ensure_ascii=False)
- ✅ Cartelle create automaticamente se mancanti

**Esecuzione:**
```bash
# Forma semplice
python scripts/process_csv.py

# Con parametri personalizzati
python scripts/process_csv.py /path/to/csv.csv /path/to/output.json
```

---

## ✨ Funzionalità Avanzate

### Ricerca Modelli
```typescript
const { searchModels } = useModels();

const results = searchModels("candido");
// Cerca in nome e descrizioni di tutte le lingue
```

### Accesso Diretto a Modello
```typescript
const { getModelById } = useModels();

const model = getModelById(1);
// Restituisce FashionModel o undefined
```

### Nomi Colori Localizzati
```typescript
import { getColorName } from './types/model';

const name = getColorName(
  colorVariant,
  'IT',    // lingua richiesta
  'EN'     // fallback
);
```

---

## 🚀 Deployment Checklist

- [ ] CSV 226Multi_2.csv nel root directory
- [ ] Eseguito `python scripts/process_csv.py`
- [ ] `src/data/models.json` generato e validato
- [ ] `src/public/data/models.json` disponibile per client
- [ ] App wrappato in `<LanguageProvider>`
- [ ] `useModels()` hook inizializzato
- [ ] `LanguageSwitcher` inserito in UI
- [ ] Componenti Model* importati e utilizzati
- [ ] Build e test multilingue completati
- [ ] Immagini varianti colore raggiungibili

---

## 🔍 Troubleshooting

### "Modelli non caricano"
- ✅ Verifica che `models.json` sia in `public/data/`
- ✅ Controlla console per errori fetch
- ✅ Valida JSON con `python -m json.tool src/data/models.json`

### "Immagini colori non visibili"
- ✅ Valida URL in CSV (column "Colore URL Immagine")
- ✅ Controlla CORS se remote
- ✅ Fallback automatico a placeholder champagne

### "Testi non tradotti"
- ✅ Verifica che CSV abbia righe per tutte le lingue
- ✅ Controlla codici lingua (IT, EN, RU uppercase)
- ✅ Messaggio fallback è normale se campo vuoto in CSV

### "Errore Python: "Lingua" colonna non trovata"
- ✅ Verifica nomi colonne esatti in CSV
- ✅ Case-sensitive: deve essere "Lingua", non "lingua"
- ✅ File deve essere UTF-8, non Latin-1

---

## 📚 Riferimenti Componenti

| Componente | Scopo | Props |
|---|---|---|
| `ModelCard` | Anteprima compatta modello | `model: FashionModel` |
| `ColorVariantGallery` | Galleria colori completa | `model: FashionModel` |
| `ModelDetail` | Vista dettagliata modello | `model: FashionModel` |
| `SalesAdvice` | Consigli di vendita | `model: FashionModel` |
| `ObjectionHandling` | Gestione obiezioni | `model: FashionModel` |
| `LanguageSwitcher` | Cambio lingua | (nessuna) |

---

## 🎯 Prossimi Passi

1. **Carica CSV** con dati completi
2. **Genera JSON** con `process_csv.py`
3. **Integra Provider** nella tua App
4. **Testa lingue** e fallback
5. **Customizza styling** se necessario
6. **Deploy** con fiducia! 🚀

---

**Buon lavoro! La tua architettura multilingue è pronta!** 🌍✨
