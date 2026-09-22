import { useState } from "react";
import { ImageIcon } from "lucide-react";
import { useLanguage } from "@/lib/language";
import { cn } from "@/lib/utils";

interface Props {
  src: string | null;
  alt: string;
  className?: string;
  onClick?: () => void;
}

export function ImageTile({ src, alt, className, onClick }: Props) {
  const [failed, setFailed] = useState(false);
  const { t } = useLanguage();
  const broken = !src || failed;

  return (
    <div
      className={cn(
        "relative flex items-center justify-center overflow-hidden rounded-sm border border-gold/30 bg-champagne",
        onClick && !broken && "cursor-zoom-in",
        className,
      )}
      onClick={broken ? undefined : onClick}
    >
      {broken ? (
        <div className="flex flex-col items-center gap-1 p-3 text-center">
          <ImageIcon className="h-5 w-5 text-gold" aria-hidden />
          <span className="text-[10px] tracking-wide text-muted-foreground">{t("noImage")}</span>
        </div>
      ) : (
        <img
          src={src!}
          alt={alt}
          loading="lazy"
          onError={() => setFailed(true)}
          className="h-full w-full object-cover"
        />
      )}
    </div>
  );
}
