/**
 * ObjectionHandling component for displaying sales objection responses.
 * Provides guidance for handling customer objections with multilingual support.
 */

import React from 'react';
import { FashionModel, getLocalizedContent } from '../types/model';
import { useLanguage } from '../contexts/LanguageContext';
import { Shield } from 'lucide-react';

interface ObjectionHandlingProps {
  model: FashionModel;
}

/**
 * Displays objection handling guidance with fallback for missing translations.
 */
const ObjectionHandling: React.FC<ObjectionHandlingProps> = ({ model }) => {
  const { currentLanguage, fallbackLanguage } = useLanguage();

  const handling = getLocalizedContent(
    model.objectionHandling,
    currentLanguage,
    fallbackLanguage
  );

  if (!handling) {
    return (
      <section>
        <div className="flex items-center gap-2 mb-3">
          <Shield className="w-5 h-5 text-blue-600" />
          <h2 className="text-xl font-semibold text-gray-900">
            Gestione Obiezioni
          </h2>
        </div>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-800 italic">
            Contenuto non disponibile in questa lingua
          </p>
        </div>
      </section>
    );
  }

  return (
    <section>
      <div className="flex items-center gap-2 mb-3">
        <Shield className="w-5 h-5 text-blue-600" />
        <h2 className="text-xl font-semibold text-gray-900">
          Gestione Obiezioni
        </h2>
      </div>
      <div className="bg-blue-50 border-l-4 border-blue-600 rounded-r-lg p-4">
        <div className="prose prose-sm max-w-none text-gray-700">
          <p className="whitespace-pre-wrap mb-0">{handling}</p>
        </div>
      </div>
    </section>
  );
};

export default ObjectionHandling;
