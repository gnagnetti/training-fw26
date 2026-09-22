/**
 * ColorVariantGallery component for displaying all color variants of a model.
 * Includes image fallback, error handling, and multilingual color names.
 */

import React, { useState } from 'react';
import { FashionModel, ColorVariant, getColorName } from '../types/model';
import { useLanguage } from '../contexts/LanguageContext';
import { AlertCircle } from 'lucide-react';

interface ColorVariantGalleryProps {
  model: FashionModel;
}

/**
 * Gallery displaying all color variants with:
 * - Multilingual color names
 * - Image error handling with fallback
 * - Responsive grid layout
 */
const ColorVariantGallery: React.FC<ColorVariantGalleryProps> = ({ model }) => {
  const { currentLanguage, fallbackLanguage } = useLanguage();
  const [failedImages, setFailedImages] = useState<Set<string>>(new Set());

  const handleImageError = (colorCode: string) => {
    setFailedImages((prev) => new Set(prev).add(colorCode));
  };

  if (model.colorVariants.length === 0) {
    return (
      <div className="py-8 text-center">
        <p className="text-sm text-gray-500">
          Nessuna variante di colore disponibile
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h4 className="font-semibold text-gray-900">Varianti Colore</h4>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {model.colorVariants.map((variant) => (
          <ColorVariantCard
            key={variant.code}
            variant={variant}
            currentLanguage={currentLanguage}
            fallbackLanguage={fallbackLanguage}
            isFailed={failedImages.has(variant.code)}
            onImageError={() => handleImageError(variant.code)}
          />
        ))}
      </div>
    </div>
  );
};

interface ColorVariantCardProps {
  variant: ColorVariant;
  currentLanguage: string;
  fallbackLanguage: string;
  isFailed: boolean;
  onImageError: () => void;
}

/**
 * Individual color variant card with image and details.
 */
const ColorVariantCard: React.FC<ColorVariantCardProps> = ({
  variant,
  currentLanguage,
  fallbackLanguage,
  isFailed,
  onImageError,
}) => {
  const colorName = getColorName(variant, currentLanguage, fallbackLanguage);
  const hasImage = variant.imageUrl && !isFailed;

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow">
      {/* Image Container */}
      <div className="aspect-square bg-[#F4F0EA] flex items-center justify-center relative overflow-hidden">
        {hasImage ? (
          <img
            src={variant.imageUrl}
            alt={colorName || `Color ${variant.code}`}
            className="w-full h-full object-cover"
            onError={onImageError}
          />
        ) : (
          <div className="flex flex-col items-center justify-center gap-2 p-4 text-center">
            <AlertCircle className="w-6 h-6 text-gray-400" />
            <span className="text-xs text-gray-500">
              Immagine non disponibile
            </span>
          </div>
        )}
      </div>

      {/* Color Details */}
      <div className="p-3 bg-white">
        {colorName && (
          <h5 className="text-sm font-medium text-gray-900 truncate">
            {colorName}
          </h5>
        )}
        <p className="text-xs text-gray-600 font-mono mt-1">{variant.code}</p>

        {!colorName && (
          <p className="text-xs text-gray-500 italic">
            Nome non disponibile
          </p>
        )}
      </div>
    </div>
  );
};

export default ColorVariantGallery;
