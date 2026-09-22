/**
 * ModelCard component for displaying a single fashion model.
 * Shows model name, description, and color variants with multilingual support.
 */

import React, { useState } from 'react';
import { FashionModel, getLocalizedContent, getColorName } from '../types/model';
import { useLanguage } from '../contexts/LanguageContext';
import ColorVariantGallery from './ColorVariantGallery';
import { ChevronDown, ChevronUp } from 'lucide-react';

interface ModelCardProps {
  model: FashionModel;
  onClick?: () => void;
}

/**
 * Expandable card displaying model details.
 */
const ModelCard: React.FC<ModelCardProps> = ({ model, onClick }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const { currentLanguage, fallbackLanguage } = useLanguage();

  const description = getLocalizedContent(
    model.descriptions,
    currentLanguage,
    fallbackLanguage
  );

  return (
    <div
      className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow"
      onClick={() => {
        setIsExpanded(!isExpanded);
        onClick?.();
      }}
    >
      {/* Header */}
      <div className="p-4 cursor-pointer flex items-center justify-between">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900">{model.name}</h3>
          {description && (
            <p className="text-sm text-gray-600 mt-1 line-clamp-2">
              {description}
            </p>
          )}
        </div>
        <button
          className="ml-4 p-2 hover:bg-gray-100 rounded-md transition-colors"
          onClick={(e) => {
            e.stopPropagation();
            setIsExpanded(!isExpanded);
          }}
        >
          {isExpanded ? (
            <ChevronUp className="w-5 h-5 text-gray-500" />
          ) : (
            <ChevronDown className="w-5 h-5 text-gray-500" />
          )}
        </button>
      </div>

      {/* Color Variants Preview */}
      {model.colorVariants.length > 0 && (
        <div className="px-4 pb-4">
          <p className="text-xs font-medium text-gray-500 uppercase mb-2">
            Varianti Colore ({model.colorVariants.length})
          </p>
          <div className="flex flex-wrap gap-2">
            {model.colorVariants.slice(0, 6).map((variant) => (
              <div key={variant.code} className="flex items-center gap-1">
                {variant.imageUrl ? (
                  <img
                    src={variant.imageUrl}
                    alt={getColorName(variant, currentLanguage, fallbackLanguage)}
                    className="w-8 h-8 rounded border border-gray-200"
                    onError={(e) => {
                      e.currentTarget.style.display = 'none';
                    }}
                  />
                ) : (
                  <div className="w-8 h-8 rounded border border-gray-200 bg-[#F4F0EA] flex items-center justify-center">
                    <span className="text-xs text-gray-400">–</span>
                  </div>
                )}
                <span className="text-xs text-gray-600">{variant.code}</span>
              </div>
            ))}
            {model.colorVariants.length > 6 && (
              <span className="text-xs text-gray-500">
                +{model.colorVariants.length - 6}
              </span>
            )}
          </div>
        </div>
      )}

      {/* Expanded Details */}
      {isExpanded && (
        <div className="border-t border-gray-200 p-4 space-y-4 bg-gray-50">
          <ColorVariantGallery model={model} />
        </div>
      )}
    </div>
  );
};

export default ModelCard;
