/**
 * ModelDetail component for displaying comprehensive model information.
 * Shows descriptions, sales advice, and objection handling with multilingual support.
 */

import React from 'react';
import { FashionModel, getLocalizedContent } from '../types/model';
import { useLanguage } from '../contexts/LanguageContext';
import SalesAdvice from './SalesAdvice';
import ObjectionHandling from './ObjectionHandling';

interface ModelDetailProps {
  model: FashionModel;
}

/**
 * Detailed view of a single model with all multilingual content sections.
 */
const ModelDetail: React.FC<ModelDetailProps> = ({ model }) => {
  const { currentLanguage, fallbackLanguage } = useLanguage();

  const description = getLocalizedContent(
    model.descriptions,
    currentLanguage,
    fallbackLanguage
  );

  return (
    <div className="space-y-6">
      {/* Model Header */}
      <div className="border-b border-gray-200 pb-4">
        <h1 className="text-3xl font-bold text-gray-900">{model.name}</h1>
        <p className="text-sm text-gray-500 mt-2">ID: {model.id}</p>
      </div>

      {/* Description Section */}
      {description && (
        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">
            Descrizione
          </h2>
          <div className="prose prose-sm max-w-none text-gray-700 bg-gray-50 p-4 rounded-lg">
            <p className="whitespace-pre-wrap">{description}</p>
          </div>
        </section>
      )}

      {/* Sales Advice Section */}
      <SalesAdvice model={model} />

      {/* Objection Handling Section */}
      <ObjectionHandling model={model} />
    </div>
  );
};

export default ModelDetail;
