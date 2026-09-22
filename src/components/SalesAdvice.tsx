/**
 * SalesAdvice component for displaying model-specific sales tips.
 * Handles multilingual content with elegant fallback messaging.
 */

import React from 'react';
import { FashionModel, getLocalizedContent } from '../types/model';
import { useLanguage } from '../contexts/LanguageContext';
import { Lightbulb } from 'lucide-react';

interface SalesAdviceProps {
  model: FashionModel;
}

/**
 * Displays sales advice with fallback handling for missing translations.
 */
const SalesAdvice: React.FC<SalesAdviceProps> = ({ model }) => {
  const { currentLanguage, fallbackLanguage } = useLanguage();

  const advice = getLocalizedContent(
    model.salesAdvice,
    currentLanguage,
    fallbackLanguage
  );

  if (!advice) {
    return (
      <section>
        <div className="flex items-center gap-2 mb-3">
          <Lightbulb className="w-5 h-5 text-amber-500" />
          <h2 className="text-xl font-semibold text-gray-900">
            Consigli di Vendita
          </h2>
        </div>
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <p className="text-sm text-amber-800 italic">
            Contenuto non disponibile in questa lingua
          </p>
        </div>
      </section>
    );
  }

  return (
    <section>
      <div className="flex items-center gap-2 mb-3">
        <Lightbulb className="w-5 h-5 text-amber-500" />
        <h2 className="text-xl font-semibold text-gray-900">
          Consigli di Vendita
        </h2>
      </div>
      <div className="bg-amber-50 border-l-4 border-amber-500 rounded-r-lg p-4">
        <div className="prose prose-sm max-w-none text-gray-700">
          <p className="whitespace-pre-wrap mb-0">{advice}</p>
        </div>
      </div>
    </section>
  );
};

export default SalesAdvice;
