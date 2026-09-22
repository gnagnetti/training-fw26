/**
 * LanguageSwitcher component for selecting the current display language.
 * Displays available languages and allows dynamic switching.
 */

import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Globe } from 'lucide-react';

/**
 * Language selector dropdown with all available languages.
 */
const LanguageSwitcher: React.FC = () => {
  const { currentLanguage, setCurrentLanguage, availableLanguages } =
    useLanguage();

  return (
    <div className="flex items-center gap-2">
      <Globe className="w-4 h-4 text-gray-600" />
      <select
        value={currentLanguage}
        onChange={(e) => setCurrentLanguage(e.target.value)}
        className="px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-900 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        {availableLanguages.map((lang) => (
          <option key={lang} value={lang}>
            {getLanguageName(lang)}
          </option>
        ))}
      </select>
    </div>
  );
};

/**
 * Get display name for a language code.
 */
function getLanguageName(code: string): string {
  const names: Record<string, string> = {
    IT: 'Italiano',
    EN: 'English',
    RU: 'Русский',
    FR: 'Français',
    DE: 'Deutsch',
    ES: 'Español',
    PT: 'Português',
    ZH: '中文',
    JA: '日本語',
    KO: '한국어',
  };
  return names[code] || code;
}

export default LanguageSwitcher;
