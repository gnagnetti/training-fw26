import { createFileRoute } from "@tanstack/react-router";
import { ModelPicker } from "@/components/ModelPicker";
import { useLanguage } from "@/lib/language";
import { modelIndex } from "@/lib/models";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Training Material Fall Winter 2026/2027 | Luisa Spagnoli" },
      {
        name: "description",
        content:
          "Search all 273 Luisa Spagnoli FW 2026/2027 models and open the full retail training sheet in English or Russian.",
      },
      { property: "og:title", content: "Training Material Fall Winter 2026/2027 | Luisa Spagnoli" },
      {
        property: "og:description",
        content:
          "Search all 273 models of the Luisa Spagnoli FW 2026/2027 collection and open their training sheets.",
      },
    ],
  }),
  component: Index,
});

function Index() {
  const { t } = useLanguage();

  return (
    <main className="mx-auto max-w-2xl px-4 py-10">
      <h1 className="font-display text-3xl leading-tight font-semibold text-foreground">
        {t("pageTitle")}
      </h1>
      <div className="mt-3 h-px w-16 bg-gold" />
      <p className="mt-5 text-sm leading-relaxed text-muted-foreground">{t("intro")}</p>

      <div className="mt-8 rounded-sm border border-border bg-card p-5 shadow-sm">
        <ModelPicker />
        <p className="mt-4 text-center text-[11px] tracking-widest text-muted-foreground uppercase">
          {modelIndex.length} {t("models")}
        </p>
      </div>
    </main>
  );
}
