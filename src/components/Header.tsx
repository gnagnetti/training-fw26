import { Link } from "@tanstack/react-router";
import { Globe, ChevronDown, Check } from "lucide-react";
import { useLanguage, LANGUAGES } from "@/lib/language";
import { cn } from "@/lib/utils";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export function Header() {
  const { lang, setLang, t, isRtl } = useLanguage();
  const currentLang = LANGUAGES.find((l) => l.code === lang) ?? LANGUAGES[0];

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/90 backdrop-blur-md">
      <div className="mx-auto flex max-w-2xl items-center justify-between gap-3 px-4 py-3">
        <Link to="/" className="min-w-0">
          <p className="font-display text-base leading-none font-semibold tracking-[0.22em] text-foreground uppercase">
            Luisa Spagnoli
          </p>
          <p className="mt-1 truncate text-[11px] tracking-wide text-muted-foreground">
            {t("brandSub")}
          </p>
        </Link>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <button
              type="button"
              className={cn(
                "group flex shrink-0 items-center gap-1.5 rounded-full border border-gold/40 bg-card/60 px-3 py-1 text-xs font-semibold tracking-wide text-foreground shadow-2xs backdrop-blur-xs transition-all hover:border-gold hover:bg-gold/10 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-gold",
              )}
              aria-label="Select language"
            >
              <Globe className="h-3.5 w-3.5 text-gold shrink-0 transition-transform group-hover:rotate-12" />
              <span className="font-medium">{currentLang.name}</span>
              <ChevronDown className="h-3 w-3 text-muted-foreground transition-transform group-data-[state=open]:rotate-180" />
            </button>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            align={isRtl ? "start" : "end"}
            className="min-w-[170px] border border-gold/30 bg-card/95 p-1 backdrop-blur-md shadow-lg"
          >
            {LANGUAGES.map((l) => {
              const isSelected = lang === l.code;
              return (
                <DropdownMenuItem
                  key={l.code}
                  onClick={() => setLang(l.code)}
                  className={cn(
                    "flex cursor-pointer items-center justify-between gap-2 rounded-sm px-2.5 py-1.5 text-xs transition-colors",
                    isSelected
                      ? "bg-gold/15 font-semibold text-foreground"
                      : "text-muted-foreground hover:bg-gold/10 hover:text-foreground",
                  )}
                >
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-mono uppercase text-gold/80 w-5">
                      {l.code}
                    </span>
                    <span>{l.name}</span>
                  </div>
                  {isSelected && <Check className="h-3.5 w-3.5 text-gold shrink-0" />}
                </DropdownMenuItem>
              );
            })}
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
