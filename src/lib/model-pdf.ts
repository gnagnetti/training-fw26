import { jsPDF } from "jspdf";
import fontUrl from "@/assets/fonts/DejaVuSans.ttf?url";
import { heroImage, getLookTitle, getLookText, getModelObjections, type Lang, type Model } from "./models";

const copy: Record<
  Lang,
  {
    material: string;
    description: string;
    colors: string;
    styling: string;
    advice: string;
    objections: string;
    noImage: string;
    answer: string;
  }
> = {
  en: {
    material: "Training Material FW 2026/2027",
    description: "Description",
    colors: "Color Variants",
    styling: "Styling / Combinations",
    advice: "Sales Advice",
    objections: "Objection Handling",
    noImage: "Image unavailable",
    answer: "Response",
  },
  ru: {
    material: "Учебные материалы Осень-Зима 2026/2027",
    description: "Описание",
    colors: "Варианты цвета",
    styling: "Стайлинг и сочетания",
    advice: "Советы по продажам",
    objections: "Управление возражениями",
    noImage: "Изображение недоступно",
    answer: "Ответ",
  },
  ar: {
    material: "المواد التدريبية خريف وشتاء 2026/2027",
    description: "الوصف",
    colors: "خيارات الألوان",
    styling: "التنسيق والمجموعات",
    advice: "نصائح البيع",
    objections: "التعامل مع الاعتراضات",
    noImage: "الصورة غير متوفرة",
    answer: "الإجابة",
  },
  hy: {
    material: "Ուսումնական նյութեր Աշուն-Ձմեռ 2026/2027",
    description: "Նկարագրություն",
    colors: "Գույնի տարբերակներ",
    styling: "Ոճավորում և համադրություններ",
    advice: "Վաճառքի խորհուրդներ",
    objections: "Առարկությունների հաղթահարում",
    noImage: "Պատկերը հասանելի չէ",
    answer: "Պատասխան",
  },
  ka: {
    material: "სასწავლო მასალები შემოდგომა-ზამთარი 2026/2027",
    description: "აღწერა",
    colors: "ფერების ვარიანტები",
    styling: "სტილი და კომბინაციები",
    advice: "გაყიდვების რჩევები",
    objections: "შედავებთან მუშაობა",
    noImage: "სურათი მიუწვდომელია",
    answer: "პასუხი",
  },
  uk: {
    material: "Навчальні матеріали Осінь-Зима 2026/2027",
    description: "Опис",
    colors: "Варіанти кольорів",
    styling: "Стилізація та комбінації",
    advice: "Поради з продажу",
    objections: "Робота із запереченнями",
    noImage: "Зображення недоступне",
    answer: "Відповідь",
  },
  lv: {
    material: "Mācību materiāli Rudens-Ziema 2026/2027",
    description: "Apraksts",
    colors: "Krāsu varianti",
    styling: "Stils un kombinācijas",
    advice: "Pārdošanas padomi",
    objections: "Iebildumu apstrāde",
    noImage: "Attēls nav pieejams",
    answer: "Atbilde",
  },
  lt: {
    material: "Mokymo medžiaga Ruduo-Žiema 2026/2027",
    description: "Aprašymas",
    colors: "Spalvų variantai",
    styling: "Stilius ir deriniai",
    advice: "Pardavimo patarimai",
    objections: "Prieštaravimų valdymas",
    noImage: "Vaizdas nepasiekiamas",
    answer: "Atsakymas",
  },
  pl: {
    material: "Materiały szkoleniowe FW 2026/2027",
    description: "Opis",
    colors: "Warianty kolorystyczne",
    styling: "Styling / Połączenia",
    advice: "Wskazówki sprzedażowe",
    objections: "Zarządzanie obiekcjami",
    noImage: "Zdjęcie niedostępne",
    answer: "Odpowiedź",
  },
};

function cleanPdfText(value: string) {
  return value
    .replace(/!\[[^\]]*]\([^)]*\)\s*\{[^}]*\}/g, "")
    .replace(/!\[[^\]]*]\([^)]*\)/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function arrayBufferToBase64(buffer: ArrayBuffer) {
  const bytes = new Uint8Array(buffer);
  let binary = "";
  const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) {
    binary += String.fromCharCode(...bytes.subarray(i, i + chunk));
  }
  return btoa(binary);
}

async function loadImage(url: string | null) {
  if (!url) return null;
  try {
    const source = new URL(url);
    const requestUrl =
      source.hostname === "cdn.jooraccess.com"
        ? `/api/public/image?url=${encodeURIComponent(url)}`
        : url;
    const response = await fetch(requestUrl);
    if (!response.ok) return null;
    const blob = await response.blob();
    const dataUrl = await new Promise<string>((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => (typeof reader.result === "string" ? resolve(reader.result) : reject());
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
    const dimensions = await new Promise<{ width: number; height: number }>((resolve, reject) => {
      const image = new Image();
      image.onload = () => resolve({ width: image.naturalWidth, height: image.naturalHeight });
      image.onerror = reject;
      image.src = dataUrl;
    });
    return { dataUrl, ...dimensions };
  } catch {
    return null;
  }
}

export async function downloadModelPdf(model: Model, lang: Lang) {
  const text = copy[lang];
  const pdf = new jsPDF({ unit: "mm", format: "a4", compress: true });
  const font = await fetch(fontUrl).then((response) => response.arrayBuffer());
  pdf.addFileToVFS("DejaVuSans.ttf", arrayBufferToBase64(font));
  pdf.addFont("DejaVuSans.ttf", "DejaVu", "normal");
  pdf.setFont("DejaVu", "normal");

  const margin = 16;
  const pageWidth = 210;
  const pageHeight = 297;
  const contentWidth = pageWidth - margin * 2;
  let y = 18;

  const newPage = () => {
    pdf.addPage();
    pdf.setFont("DejaVu", "normal");
    y = 18;
  };
  const ensure = (height: number) => {
    if (y + height > pageHeight - 16) newPage();
  };
  const lines = (value: string, width = contentWidth, size = 9) => {
    pdf.setFontSize(size);
    return pdf.splitTextToSize(cleanPdfText(value), width) as string[];
  };
  const paragraph = (value: string, options?: { indent?: number; size?: number; gap?: number }) => {
    const indent = options?.indent ?? 0;
    const size = options?.size ?? 9;
    const gap = options?.gap ?? 4;
    const wrapped = lines(value, contentWidth - indent, size);
    const height = wrapped.length * (size * 0.42) + gap;
    ensure(height);
    pdf.setTextColor(45, 43, 39);
    pdf.text(wrapped, margin + indent, y);
    y += height;
  };
  const heading = (value: string, followingHeight = 0) => {
    ensure(14 + followingHeight);
    y += 4;
    pdf.setFontSize(12);
    pdf.setTextColor(151, 116, 56);
    pdf.text(value.toUpperCase(), margin, y);
    y += 3;
    pdf.setDrawColor(151, 116, 56);
    pdf.line(margin, y, margin + 18, y);
    y += 7;
  };
  const imageBox = async (
    url: string | null,
    x: number,
    top: number,
    width: number,
    height: number,
  ) => {
    const image = await loadImage(url);
    pdf.setDrawColor(220, 215, 205);
    pdf.rect(x, top, width, height);
    if (!image) {
      pdf.setFontSize(7);
      pdf.setTextColor(130, 126, 118);
      pdf.text(text.noImage, x + width / 2, top + height / 2, { align: "center" });
      return;
    }
    const ratio = Math.min((width - 2) / image.width, (height - 2) / image.height);
    const drawWidth = image.width * ratio;
    const drawHeight = image.height * ratio;
    pdf.addImage(
      image.dataUrl,
      x + (width - drawWidth) / 2,
      top + (height - drawHeight) / 2,
      drawWidth,
      drawHeight,
    );
  };

  pdf.setTextColor(34, 32, 29);
  pdf.setFontSize(18);
  pdf.text("LUISA SPAGNOLI", margin, y);
  y += 7;
  pdf.setFontSize(8);
  pdf.setTextColor(105, 101, 94);
  pdf.text(text.material, margin, y);
  y += 12;
  pdf.setFontSize(22);
  pdf.setTextColor(34, 32, 29);
  pdf.text(model.name, margin, y);
  pdf.setFontSize(9);
  pdf.setTextColor(151, 116, 56);
  pdf.text(`ID #${model.id}`, pageWidth - margin, y, { align: "right" });
  y += 8;

  const cover = heroImage(model);
  if (cover) {
    ensure(78);
    await imageBox(cover, margin, y, contentWidth, 74);
    y += 78;
  }

  const description = model.description[lang] || model.description.en || model.description.ru || "";
  if (description) {
    heading(text.description);
    paragraph(description);
  }

  if (model.colors.length) {
    heading(text.colors);
    for (let i = 0; i < model.colors.length; i += 3) {
      const group = model.colors.slice(i, i + 3);
      ensure(62);
      for (let column = 0; column < group.length; column += 1) {
        const color = group[column];
        if (!color) continue;
        const x = margin + column * 58;
        await imageBox(color.imageUrl, x, y, 50, 46);
        pdf.setFontSize(8);
        pdf.setTextColor(45, 43, 39);
        pdf.text(lines(`${color.name} (${color.code})`, 50, 8), x, y + 51);
      }
      y += 62;
    }
  }

  if (model.looks.length) {
    heading(text.styling, 45);
    for (const look of model.looks) {
      const lookTitle = getLookTitle(look, lang);
      const lookText = getLookText(look, lang);
      const lookLines = lines(lookText, contentWidth - 8, 8.5);
      const imageRows = look.items.length ? Math.ceil(look.items.length / 4) : 0;
      const estimated = 10 + lookLines.length * 3.6 + imageRows * 53;
      ensure(Math.min(estimated, pageHeight - 34));
      const top = y;
      pdf.setFillColor(249, 248, 245);
      pdf.setDrawColor(220, 215, 205);
      pdf.roundedRect(
        margin,
        top,
        contentWidth,
        Math.min(estimated, pageHeight - top - 16),
        1,
        1,
        "FD",
      );
      y += 7;
      if (lookTitle) paragraph(lookTitle, { indent: 4, size: 9, gap: 2 });
      if (lookText) paragraph(lookText, { indent: 4, size: 8.5, gap: 4 });
      for (let i = 0; i < look.items.length; i += 4) {
        const group = look.items.slice(i, i + 4);
        ensure(51);
        for (let column = 0; column < group.length; column += 1) {
          const item = group[column];
          if (!item) continue;
          const x = margin + 4 + column * 42;
          await imageBox(item.imageUrl, x, y, 36, 38);
          pdf.setFontSize(7);
          pdf.setTextColor(45, 43, 39);
          pdf.text(lines(`${item.name} ${item.code}`.trim(), 36, 7), x, y + 42);
        }
        y += 51;
      }
      y += 5;
    }
  }

  const advice =
    (model.advice[lang]?.length
      ? model.advice[lang]
      : model.advice.en?.length
        ? model.advice.en
        : model.advice.ru) || [];
  if (advice.length) {
    const firstAdvice = advice[0] ?? "";
    heading(text.advice, lines(`1. ${firstAdvice}`, contentWidth, 9).length * 3.8 + 8);
    advice.forEach((item, index) => paragraph(`${index + 1}. ${item}`));
  }

  const objections = getModelObjections(model, lang);

  if (objections.length) {
    const firstObjection = objections[0];
    const firstObjectionHeight = firstObjection
      ? lines(`1. ${firstObjection.q}`, contentWidth, 9).length * 3.8 +
        lines(`${text.answer}: ${firstObjection.a}`, contentWidth - 4, 8.5).length * 3.6 +
        12
      : 20;
    heading(text.objections, firstObjectionHeight);
    objections.forEach((item, index) => {
      paragraph(`${index + 1}. ${item.q}`, { size: 9, gap: 2 });
      paragraph(`${text.answer}: ${item.a}`, { indent: 4, size: 8.5, gap: 6 });
    });
  }

  const totalPages = pdf.getNumberOfPages();
  for (let page = 1; page <= totalPages; page += 1) {
    pdf.setPage(page);
    pdf.setFont("DejaVu", "normal");
    pdf.setFontSize(7);
    pdf.setTextColor(130, 126, 118);
    pdf.text(`${model.name} · ${page}/${totalPages}`, pageWidth - margin, pageHeight - 8, {
      align: "right",
    });
  }
  pdf.save(`${model.name.replace(/[^a-z0-9а-яё]+/gi, "-").replace(/^-|-$/g, "")}-${lang}.pdf`);
}
