import index from "@/data/index.json";

export type Lang = "en" | "ru" | "ar" | "hy" | "ka" | "uk" | "lv" | "lt" | "pl";

export interface ColorVariant {
  name: string;
  code: string;
  imageUrl: string | null;
}

export interface OutfitItem {
  name: string;
  code: string;
  imageUrl: string | null;
  modelId?: number;
}

export interface Look {
  title: Record<string, string | null> | string | null;
  text: Record<string, string> | string;
  items: OutfitItem[];
}

export function getLookTitle(look: Look, lang: string): string | null {
  const title = look.title;
  if (!title) return null;
  if (typeof title === "string") return title;
  return title[lang] || title.en || title.ru || null;
}

export function getLookText(look: Look, lang: string): string {
  const text = look.text;
  if (!text) return "";
  if (typeof text === "string") return text;
  return text[lang] || text.en || text.ru || "";
}

export interface Objection {
  q: string;
  a: string;
}

export interface Model {
  id: number;
  name: string;
  description: Record<string, string>;
  colors: ColorVariant[];
  looks: Look[];
  advice: Record<string, string[]>;
  objections: Record<string, Objection[]>;
}

export const modelIndex: { id: number; name: string }[] = index;

const files = import.meta.glob<{ default: Model }>("../data/models/*.json");

export async function loadModel(id: number): Promise<Model | null> {
  const loader = files[`../data/models/${id}.json`];
  if (!loader) return null;
  const mod = await loader();
  return mod.default;
}

export function heroImage(model: Model): string | null {
  return model.colors.find((c) => c.imageUrl)?.imageUrl ?? null;
}

export function cleanObjectionText(s: string): string {
  if (!s) return "";
  return s
    .replace(/^[\s,;«»“”"':\-–—\x9d]+|[\s,;«»“”"':\-–—\x9d]+$/g, "")
    .replace(/^(?:Objection\s*\d*\s*[:\-]|Response\s*[:\-]|Возражение\s*[:\-]|Ответ\s*[:\-]|الاعتراض\s*[:\-]|الرد\s*[:\-])\s*/i, "")
    .replace(/\s{2,}/g, " ")
    .trim();
}

export function normalizeObjections(items: Objection[]): Objection[] {
  if (!items || !items.length) return [];
  const result: Objection[] = [];

  for (const item of items) {
    const rawQ = cleanObjectionText(item.q || "");
    const rawA = cleanObjectionText(item.a || "");

    if (rawQ && rawA) {
      const aWithPeriod = /[.!?…]$/.test(rawA) ? rawA : `${rawA}.`;
      result.push({ q: rawQ, a: aWithPeriod });
      continue;
    }

    const textToParse = rawA || rawQ;
    if (!textToParse) continue;

    // 1. Try bracket format [Q] -> A
    if (textToParse.includes("[") && textToParse.includes("]")) {
      const bracketRegex = /\[\s*(.+?)\s*\]\s*(?:->|–>|→|:)\s*([^\[]+)/gs;
      let match;
      let matchedAny = false;
      while ((match = bracketRegex.exec(textToParse)) !== null) {
        const q = cleanObjectionText(match[1]);
        const a = cleanObjectionText(match[2]);
        if (q && a) {
          matchedAny = true;
          const aWithPeriod = /[.!?…]$/.test(a) ? a : `${a}.`;
          result.push({ q, a: aWithPeriod });
        }
      }
      if (matchedAny) continue;
    }

    // 2. Try Objection: ... Response: ... format
    if (/Objection\s*(?:\d*|Overcoming\s+Strategy)?\s*:/i.test(textToParse)) {
      const objRegex = /(?:^|\s+)Objection\s*(?:\d*|Overcoming\s+Strategy)?\s*:\s*(.+?)\s*Response\s*:\s*([^]+?)(?=(?:\s+Objection\s*(?:\d*|Overcoming\s+Strategy)?\s*:|$))/gi;
      let match;
      let matchedAny = false;
      while ((match = objRegex.exec(textToParse)) !== null) {
        const q = cleanObjectionText(match[1]);
        const a = cleanObjectionText(match[2]);
        if (q && a) {
          matchedAny = true;
          const aWithPeriod = /[.!?…]$/.test(a) ? a : `${a}.`;
          result.push({ q, a: aWithPeriod });
        }
      }
      if (matchedAny) continue;
    }

    // 3. Fallback: single item if we have some text
    if (rawA) {
      const aWithPeriod = /[.!?…]$/.test(rawA) ? rawA : `${rawA}.`;
      result.push({ q: rawQ || "—", a: aWithPeriod });
    }
  }

  return result;
}

export function getModelObjections(model: Model, lang: Lang): Objection[] {
  const list =
    model.objections?.[lang]?.length
      ? model.objections[lang]
      : model.objections?.en?.length
        ? model.objections.en
        : model.objections?.ru || [];

  return normalizeObjections(list);
}
