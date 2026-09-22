/**
 * TypeScript types and interfaces for the Fashion Model style guide application.
 * Supports dynamic multilingual content and flexible color variants.
 */

/**
 * Supported languages in the application.
 * Dynamically extracted from the dataset but includes common defaults.
 */
export type SupportedLanguage = 'IT' | 'EN' | 'RU' | string;

/**
 * Color variant with multilingual naming.
 * Each color can have translated names for each supported language.
 */
export interface ColorVariant {
  /** Translated color names keyed by language code */
  name: Record<SupportedLanguage, string>;
  
  /** Alphanumeric color code (e.g., "0101", "2449") */
  code: string;
  
  /** Direct URL to the color variant image or null if unavailable */
  imageUrl: string | null;
}

/**
 * Fashion model with full multilingual support.
 * All textual content is stored as language-keyed dictionaries.
 */
export interface FashionModel {
  /** Unique numeric identifier for the model */
  id: number;
  
  /** Commercial name of the garment (e.g., "CANDIDO") */
  name: string;
  
  /** Multilingual descriptions keyed by language code */
  descriptions: Record<SupportedLanguage, string>;
  
  /** Multilingual sales advice/tips keyed by language code */
  salesAdvice: Record<SupportedLanguage, string>;
  
  /** Multilingual objection handling guides keyed by language code */
  objectionHandling: Record<SupportedLanguage, string>;
  
  /** Array of available color variants for this model */
  colorVariants: ColorVariant[];
}

/**
 * Root data structure for the models dataset.
 * Contains metadata and all available models.
 */
export interface ModelsDataset {
  /** List of supported language codes present in the dataset */
  languages: SupportedLanguage[];
  
  /** Array of all fashion models */
  models: FashionModel[];
}

/**
 * Utility type for language-specific content with fallback.
 */
export type LocalizedContent = Record<SupportedLanguage, string>;

/**
 * Type guard to check if a key is a valid language in a LocalizedContent object.
 */
export function isValidLanguage(
  lang: string,
  content: LocalizedContent
): lang is SupportedLanguage {
  return lang in content;
}

/**
 * Get content in a specific language with fallback support.
 * 
 * @param content - Language-keyed content dictionary
 * @param language - Requested language
 * @param fallbackLanguage - Fallback language if requested is not available
 * @returns Content in requested language or fallback, or empty string if neither available
 */
export function getLocalizedContent(
  content: LocalizedContent,
  language: SupportedLanguage,
  fallbackLanguage?: SupportedLanguage
): string {
  if (language in content) {
    return content[language];
  }
  if (fallbackLanguage && fallbackLanguage in content) {
    return content[fallbackLanguage];
  }
  // Return first available language content
  const available = Object.values(content).find(v => v);
  return available || "";
}

/**
 * Get color name in a specific language with fallback.
 * 
 * @param colorVariant - Color variant object
 * @param language - Requested language
 * @param fallbackLanguage - Fallback language
 * @returns Color name or empty string if none available
 */
export function getColorName(
  colorVariant: ColorVariant,
  language: SupportedLanguage,
  fallbackLanguage?: SupportedLanguage
): string {
  return getLocalizedContent(
    colorVariant.name,
    language,
    fallbackLanguage
  );
}
