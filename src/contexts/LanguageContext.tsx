/**
 * Language context for multilingual support.
 * Provides current language and list of available languages extracted from dataset.
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import { SupportedLanguage } from '../types/model';

interface LanguageContextType {
  /** Currently selected language */
  currentLanguage: SupportedLanguage;
  
  /** Set the current language */
  setCurrentLanguage: (lang: SupportedLanguage) => void;
  
  /** Available languages extracted from dataset */
  availableLanguages: SupportedLanguage[];
  
  /** Fallback language for content not available in current language */
  fallbackLanguage: SupportedLanguage;
}

/**
 * Default languages if dataset is not yet loaded.
 */
const DEFAULT_LANGUAGES: SupportedLanguage[] = ['IT', 'EN', 'RU'];
const DEFAULT_LANGUAGE: SupportedLanguage = 'IT';
const FALLBACK_LANGUAGE: SupportedLanguage = 'EN';

export const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

interface LanguageProviderProps {
  children: React.ReactNode;
  availableLanguages?: SupportedLanguage[];
  defaultLanguage?: SupportedLanguage;
  fallbackLanguage?: SupportedLanguage;
}

/**
 * Language provider component.
 * 
 * Props:
 * - availableLanguages: List of languages from dataset (if undefined, uses defaults)
 * - defaultLanguage: Initial language (defaults to IT)
 * - fallbackLanguage: Language to use when content is not available (defaults to EN)
 */
export const LanguageProvider: React.FC<LanguageProviderProps> = ({
  children,
  availableLanguages = DEFAULT_LANGUAGES,
  defaultLanguage = DEFAULT_LANGUAGE,
  fallbackLanguage = FALLBACK_LANGUAGE,
}) => {
  const [currentLanguage, setCurrentLanguage] = useState<SupportedLanguage>(defaultLanguage);

  // Validate that current language is available, otherwise reset to default
  useEffect(() => {
    if (!availableLanguages.includes(currentLanguage)) {
      setCurrentLanguage(defaultLanguage);
    }
  }, [availableLanguages, currentLanguage, defaultLanguage]);

  const value: LanguageContextType = {
    currentLanguage,
    setCurrentLanguage,
    availableLanguages,
    fallbackLanguage,
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};

/**
 * Hook to access language context.
 * 
 * @returns Language context with current language and available options
 * @throws Error if used outside LanguageProvider
 */
export const useLanguage = (): LanguageContextType => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within LanguageProvider');
  }
  return context;
};

/**
 * Hook to get content in current language with automatic fallback.
 * 
 * @param content - Language-keyed content dictionary
 * @returns Content in current language or fallback
 */
export const useLocalizedContent = (
  content: Record<SupportedLanguage, string>
): string => {
  const { currentLanguage, fallbackLanguage } = useLanguage();

  if (currentLanguage in content) {
    return content[currentLanguage];
  }
  if (fallbackLanguage in content) {
    return content[fallbackLanguage];
  }
  // Return first available
  const available = Object.values(content).find(v => v);
  return available || '';
};
