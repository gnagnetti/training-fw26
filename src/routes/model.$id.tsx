import { useState } from "react";
import { createFileRoute, Link, notFound } from "@tanstack/react-router";
import {
  ArrowLeft,
  Award,
  CheckCircle2,
  Download,
  HelpCircle,
  Home,
  LoaderCircle,
  Sparkles,
  TrendingUp,
} from "lucide-react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";
import { ImageTile } from "@/components/ImageTile";
import { Lightbox } from "@/components/Lightbox";
import { ModelPicker } from "@/components/ModelPicker";
import {
  heroImage,
  loadModel,
  modelIndex,
  getLookTitle,
  getLookText,
  getModelObjections,
  type Model,
} from "@/lib/models";
import { useLanguage } from "@/lib/language";

export const Route = createFileRoute("/model/$id")({
  loader: async ({ params }) => {
    const model = await loadModel(Number(params.id));
    if (!model) throw notFound();
    return { model };
  },
  head: ({ loaderData }) => {
    if (!loaderData) {
      return {
        meta: [{ title: "Unavailable | Luisa Spagnoli" }, { name: "robots", content: "noindex" }],
      };
    }
    const { model } = loaderData;
    const title = `${model.name} — Training Material FW 2026/2027 | Luisa Spagnoli`;
    const description =
      model.description.en.slice(0, 155) ||
      `Training sheet for the Luisa Spagnoli ${model.name} model: colours, looks, sales advice.`;
    const image = heroImage(model);
    return {
      meta: [
        { title },
        { name: "description", content: description },
        { property: "og:title", content: title },
        { property: "og:description", content: description },
        ...(image
          ? [
              { property: "og:image", content: image },
              { name: "twitter:image", content: image },
            ]
          : []),
      ],
    };
  },
  component: ModelPage,
});

const adviceIcons = [Sparkles, Award, TrendingUp];

function ModelPage() {
  const { model } = Route.useLoaderData() as { model: Model };
  const { lang, t } = useLanguage();
  const [zoom, setZoom] = useState<{ src: string; caption: string } | null>(null);
  const [pdfState, setPdfState] = useState<"idle" | "loading" | "error">("idle");

  const hero = heroImage(model);
  const advice =
    model.advice[lang] && model.advice[lang].length > 0
      ? model.advice[lang]
      : model.advice.en && model.advice.en.length > 0
        ? model.advice.en
        : model.advice.ru || [];
  const objections = getModelObjections(model, lang);
  const description = model.description[lang] || model.description.en || model.description.ru || "";


  const handlePdfDownload = async () => {
    if (pdfState === "loading") return;
    setPdfState("loading");
    try {
      const { downloadModelPdf } = await import("@/lib/model-pdf");
      await downloadModelPdf(model, lang);
      setPdfState("idle");
    } catch {
      setPdfState("error");
    }
  };

  return (
    <main className="mx-auto max-w-2xl px-4 pt-6 pb-16">
      <div className="mb-6 rounded-sm border border-border bg-card p-5 shadow-sm">
        <ModelPicker currentModelId={model.id} />
        <p className="mt-4 text-center text-[11px] tracking-widest text-muted-foreground uppercase">
          {modelIndex.length} {t("models")}
        </p>
      </div>

      <Link
        to="/"
        className="inline-flex items-center gap-1.5 text-xs tracking-widest text-muted-foreground uppercase transition-colors hover:text-gold"
      >
        <ArrowLeft className="h-3.5 w-3.5 rtl:rotate-180" /> {t("back")}
      </Link>

      <header className="mt-4">
        <p className="text-[11px] tracking-[0.3em] text-gold uppercase">{t("analysis")}</p>
        <h1 className="font-display mt-1 text-3xl font-semibold text-foreground">{model.name}</h1>
        <span className="mt-3 inline-block rounded-full border border-gold/40 px-3 py-0.5 text-[11px] tracking-widest text-muted-foreground uppercase">
          ID #{model.id}
        </span>
      </header>

      {hero && (
        <ImageTile
          src={hero}
          alt={model.name}
          className="mt-5 aspect-[3/4] w-full"
          onClick={() => setZoom({ src: hero, caption: model.name })}
        />
      )}

      {description && (
        <Section title={t("description")}>
          <p className="text-[15px] leading-relaxed whitespace-normal text-foreground/90">
            {description}
          </p>
        </Section>
      )}

      {model.colors.length > 0 && (
        <Section title={t("colors")}>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {model.colors.map((c) => (
              <figure key={`${c.name}-${c.code}`}>
                <ImageTile
                  src={c.imageUrl}
                  alt={`${model.name} ${c.name}`}
                  className="aspect-[3/4] w-full"
                  onClick={() =>
                    c.imageUrl &&
                    setZoom({ src: c.imageUrl, caption: `${model.name} — ${c.name} (${c.code})` })
                  }
                />
                <figcaption className="mt-1.5 text-xs leading-snug text-foreground">
                  {c.name}
                  <span className="block text-[11px] text-muted-foreground">({c.code})</span>
                </figcaption>
              </figure>
            ))}
          </div>
        </Section>
      )}

      {model.looks.length > 0 && (
        <Section title={t("styling")}>
          <div className="space-y-5">
            {model.looks.map((look, i) => {
              const lookTitle = getLookTitle(look, lang);
              const lookText = getLookText(look, lang);
              return (
                <article key={i} className="rounded-sm border border-border bg-card p-4 shadow-sm">
                  {lookTitle && (
                    <h3 className="font-display text-sm tracking-wide text-gold">{lookTitle}</h3>
                  )}
                  {lookText && (
                    <p className="mt-2 text-sm leading-relaxed whitespace-normal text-foreground/90">
                      {lookText}
                    </p>
                  )}
                  {look.items.length > 0 && (
                    <div className="mt-4 -mx-1 flex snap-x gap-3 overflow-x-auto px-1 pb-1">
                      {look.items.map((it, k) => {
                        const caption = `${it.name} ${it.code}`.trim();
                        const tile = (
                          <>
                            <ImageTile
                              src={it.imageUrl}
                              alt={caption}
                              className="aspect-[3/4] w-full"
                            />
                            <p className="mt-1.5 text-xs leading-snug font-medium text-foreground">
                              {it.name}
                            </p>
                            <p className="text-[11px] text-muted-foreground">{it.code}</p>
                          </>
                        );
                        return it.modelId ? (
                          <Link
                            key={k}
                            to="/model/$id"
                            params={{ id: String(it.modelId) }}
                            className="w-28 shrink-0 snap-start"
                          >
                            {tile}
                          </Link>
                        ) : (
                          <div
                            key={k}
                            className="w-28 shrink-0 snap-start"
                            onClick={() => it.imageUrl && setZoom({ src: it.imageUrl, caption })}
                          >
                            {tile}
                          </div>
                        );
                      })}
                    </div>
                  )}
                </article>
              );
            })}
          </div>
        </Section>
      )}

      {advice.length > 0 && (
        <Section title={t("advice")}>
          <div className="space-y-3">
            {advice.map((a, i) => {
              const Icon = adviceIcons[i % adviceIcons.length] ?? Sparkles;
              return (
                <div key={i} className="rounded-sm border border-border bg-card p-4 shadow-sm">
                  <div className="flex items-center gap-2">
                    <Icon className="h-4 w-4 text-gold" aria-hidden />
                    <span className="font-display text-sm text-gold">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                  </div>
                  <p className="mt-2 text-sm leading-relaxed whitespace-normal text-foreground/90">
                    {a}
                  </p>
                </div>
              );
            })}
          </div>
        </Section>
      )}

      {objections.length > 0 && (
        <Section title={t("objections")}>
          <Accordion type="multiple" className="space-y-3">
            {objections.map((o, i) => (
              <AccordionItem
                key={i}
                value={`o-${i}`}
                className="overflow-visible rounded-sm border border-border bg-champagne px-4"
              >
                <AccordionTrigger className="gap-3 py-3 text-start hover:no-underline">
                  <span className="flex items-start gap-2">
                    <HelpCircle className="mt-0.5 h-4 w-4 shrink-0 text-gold" aria-hidden />
                    <span className="h-auto text-sm font-semibold break-words whitespace-normal text-foreground">
                      {o.q || "—"}
                    </span>
                  </span>
                </AccordionTrigger>
                <AccordionContent className="overflow-visible pb-4">
                  <div className="flex items-start gap-2 border-s-4 border-gold bg-card p-3">
                    <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-gold" aria-hidden />
                    <p className="h-auto text-sm leading-relaxed break-words whitespace-normal text-foreground/90">
                      {o.a}
                    </p>
                  </div>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </Section>
      )}

      <nav
        className="mt-12 grid gap-3 border-t border-border pt-6 sm:grid-cols-2"
        aria-label="Model actions"
      >
        <Button
          type="button"
          size="lg"
          onClick={handlePdfDownload}
          disabled={pdfState === "loading"}
        >
          {pdfState === "loading" ? (
            <LoaderCircle className="animate-spin" aria-hidden />
          ) : (
            <Download aria-hidden />
          )}
          {pdfState === "loading" ? t("preparingPdf") : t("downloadPdf")}
        </Button>
        <Button asChild variant="outline" size="lg">
          <Link to="/">
            <Home aria-hidden /> {t("returnHome")}
          </Link>
        </Button>
        {pdfState === "error" && (
          <p className="text-sm text-destructive sm:col-span-2" role="alert">
            {t("pdfError")}
          </p>
        )}
      </nav>

      <Lightbox
        src={zoom?.src ?? null}
        caption={zoom?.caption ?? ""}
        onClose={() => setZoom(null)}
      />
    </main>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mt-9">
      <h2 className="font-display text-xs tracking-[0.25em] text-muted-foreground uppercase">
        {title}
      </h2>
      <div className="mt-1 mb-4 h-px w-10 bg-gold" />
      {children}
    </section>
  );
}
