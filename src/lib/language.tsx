import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";
import type { Lang } from "./models";

const KEY = "ls-training-lang";

export interface LanguageInfo {
  code: Lang;
  name: string;
  englishName: string;
  dir: "ltr" | "rtl";
}

export const LANGUAGES: LanguageInfo[] = [
  { code: "en", name: "English", englishName: "English", dir: "ltr" },
  { code: "ru", name: "Русский", englishName: "Russian", dir: "ltr" },
  { code: "ar", name: "العربية", englishName: "Arabic", dir: "rtl" },
  { code: "hy", name: "Հայերեն", englishName: "Armenian", dir: "ltr" },
  { code: "ka", name: "ქართული", englishName: "Georgian", dir: "ltr" },
  { code: "uk", name: "Українська", englishName: "Ukrainian", dir: "ltr" },
  { code: "lv", name: "Latviešu", englishName: "Latvian", dir: "ltr" },
  { code: "lt", name: "Lietuvių", englishName: "Lithuanian", dir: "ltr" },
  { code: "pl", name: "Polski", englishName: "Polish", dir: "ltr" },
];

export function isRtlLang(lang: Lang): boolean {
  return lang === "ar";
}

interface Ctx {
  lang: Lang;
  isRtl: boolean;
  setLang: (l: Lang) => void;
  t: (k: keyof typeof strings) => string;
}

export const strings = {
  brandSub: {
    en: "Training Material FW 2026/2027",
    ru: "Учебные материалы Осень-Зима 2026/2027",
    ar: "المواد التدريبية خريف وشتاء 2026/2027",
    hy: "Ուսումնական նյութեր Աշուն-Ձմեռ 2026/2027",
    ka: "სასწავლო მასალები შემოდგომა-ზამთარი 2026/2027",
    uk: "Навчальні матеріали Осінь-Зима 2026/2027",
    lv: "Mācību materiāli Rudens-Ziema 2026/2027",
    lt: "Mokymo medžiaga Ruduo-Žiema 2026/2027",
    pl: "Materiały szkoleniowe FW 2026/2027",
  },
  pageTitle: {
    en: "Training Material Fall Winter 2026/2027",
    ru: "Учебные материалы Осень-Зима 2026/2027",
    ar: "المواد التدريبية خريف وشتاء 2026/2027",
    hy: "Ուսումնական նյութեր Աշուն-Ձմեռ 2026/2027",
    ka: "სასწავლო მასალები შემოდგომა-ზამთარი 2026/2027",
    uk: "Навчальні матеріали Осінь-Зима 2026/2027",
    lv: "Mācību materiāli Rudens-Ziema 2026/2027",
    lt: "Mokymo medžiaga Ruduo-Žiema 2026/2027",
    pl: "Materiały szkoleniowe Jesień-Zima 2026/2027",
  },
  selectModel: {
    en: "Select a model",
    ru: "Выберите модель",
    ar: "اختر موديلاً",
    hy: "Ընտրեք մոդելը",
    ka: "აირჩიეთ მოდელი",
    uk: "Оберіть модель",
    lv: "Izvēlieties modeli",
    lt: "Pasirinkite modelį",
    pl: "Wybierz model",
  },
  searchPlaceholder: {
    en: "Search model…",
    ru: "Поиск модели…",
    ar: "البحث عن موديل…",
    hy: "Մոդելի որոնում…",
    ka: "მოდელის ძებნა…",
    uk: "Пошук моделі…",
    lv: "Meklēt modeli…",
    lt: "Ieškoti modelio…",
    pl: "Szukaj modelu…",
  },
  search: {
    en: "SEARCH",
    ru: "ПОИСК",
    ar: "بحث",
    hy: "ՈՐՈՆՈՒՄ",
    ka: "ძებნა",
    uk: "ПОШУК",
    lv: "MEKLĒT",
    lt: "PAIEŠKA",
    pl: "SZUKAJ",
  },
  noResults: {
    en: "No model found",
    ru: "Модель не найдена",
    ar: "لم يتم العثور على أي موديل",
    hy: "Մոդելը չի գտնվել",
    ka: "მოდელი ვერ მოიძებნა",
    uk: "Модель не знайдено",
    lv: "Modelis nav atrasts",
    lt: "Modelis nerastas",
    pl: "Nie znaleziono modelu",
  },
  analysis: {
    en: "ANALYSIS",
    ru: "АНАЛИЗ",
    ar: "تحليل",
    hy: "ՎԵՐԼՈՒԾՈՒԹՅՈՒՆ",
    ka: "ანალიზი",
    uk: "АНАЛІЗ",
    lv: "ANALĪZE",
    lt: "ANALIZĖ",
    pl: "ANALIZA",
  },
  description: {
    en: "Description",
    ru: "Описание",
    ar: "الوصف",
    hy: "Նկարագրություն",
    ka: "აღწერა",
    uk: "Опис",
    lv: "Apraksts",
    lt: "Aprašymas",
    pl: "Opis",
  },
  colors: {
    en: "Color Variants",
    ru: "Варианты цвета",
    ar: "خيارات الألوان",
    hy: "Գույնի տարբերակներ",
    ka: "ფერების ვარიანტები",
    uk: "Варіанти кольորів",
    lv: "Krāsu varianti",
    lt: "Spalvų variantai",
    pl: "Warianty kolorystyczne",
  },
  styling: {
    en: "Styling / Combinations",
    ru: "Стайлинг и сочетания",
    ar: "التنسيق والمجموعات",
    hy: "Ոճավորում և համադրություններ",
    ka: "სტილი და კომბინაციები",
    uk: "Стилізація та комбінації",
    lv: "Stils un kombinācijas",
    lt: "Stilius ir deriniai",
    pl: "Styling / Połączenia",
  },
  advice: {
    en: "Sales Advice",
    ru: "Советы по продажам",
    ar: "نصائح البيع",
    hy: "Վաճառքի խորհուրդներ",
    ka: "გაყიდვების რჩევები",
    uk: "Поради з продажу",
    lv: "Pārdošanas padomi",
    lt: "Pardavimo patarimai",
    pl: "Wskazówki sprzedażowe",
  },
  objections: {
    en: "Objection Handling",
    ru: "Управление возражениями",
    ar: "التعامل مع الاعتراضات",
    hy: "Առարկությունների հաղթահարում",
    ka: "შედავებთან მუშაობა",
    uk: "Робота із запереченнями",
    lv: "Iebildumu apstrāde",
    lt: "Prieštaravimų valdymas",
    pl: "Zarządzanie obiekcjami",
  },
  back: {
    en: "All models",
    ru: "Все модели",
    ar: "جميع الموديلات",
    hy: "Բոլոր մոդելները",
    ka: "ყველა მოდელი",
    uk: "Усі моделі",
    lv: "Visi modeļi",
    lt: "Visi modeliai",
    pl: "Wszystkie modele",
  },
  downloadPdf: {
    en: "Download PDF",
    ru: "Скачать PDF",
    ar: "تحميل PDF",
    hy: "Ներբեռնել PDF",
    ka: "PDF-ის ჩამოტვირთვა",
    uk: "Завантажити PDF",
    lv: "Lejupielādēt PDF",
    lt: "Atsisiųsti PDF",
    pl: "Pobierz PDF",
  },
  preparingPdf: {
    en: "Preparing PDF…",
    ru: "Подготовка PDF…",
    ar: "جارٍ إعداد PDF…",
    hy: "PDF-ի պատրաստում…",
    ka: "მზადდება PDF…",
    uk: "Підготовка PDF…",
    lv: "Sagatavo PDF…",
    lt: "Ruošiamas PDF…",
    pl: "Przygotowywanie PDF…",
  },
  pdfError: {
    en: "The PDF could not be created. Please try again.",
    ru: "Не удалось создать PDF. Повторите попытку.",
    ar: "تعذر إنشاء ملف PDF. يُرجى المحاولة مرة أخرى.",
    hy: "Չհաջողվեց ստեղծել PDF-ը: Խնդրում ենք փորձել կրկին:",
    ka: "PDF-ის შექმნა ვერ მოხერხდა. გთხოვთ, სცადოთ ხელახლა.",
    uk: "Не вдалося створити PDF. Будь ласка, спробуйте знову.",
    lv: "Neizdevās izveidot PDF. Lūdzu, mēģiniet vēlreiz.",
    lt: "Nepavyko sukurti PDF. Bandykite dar kartą.",
    pl: "Nie udało się utworzyć pliku PDF. Spróbuj ponownie.",
  },
  returnHome: {
    en: "Back to all models",
    ru: "Вернуться ко всем моделям",
    ar: "العودة إلى جميع الموديلات",
    hy: "Վերադառնալ բոլոր մոդելներին",
    ka: "დაბრունება ყველა მოდელზე",
    uk: "Повернутися до всіх моделей",
    lv: "Atgriezties pie visiem modeļiem",
    lt: "Grįžti prie visų modelių",
    pl: "Powrót do wszystkich modeli",
  },
  noImage: {
    en: "No image",
    ru: "Нет изображения",
    ar: "لا توجد صورة",
    hy: "Պատկեր չկա",
    ka: "სურათი არ არის",
    uk: "Немає зображення",
    lv: "Nav attēla",
    lt: "Nėra vaizdo",
    pl: "Brak zdjęcia",
  },
  intro: {
    en: "Choose a model to open its full training sheet: description, colours, total looks, sales advice and objection handling.",
    ru: "Выберите модель, чтобы открыть полную карточку: описание, цвета, образы, советы по продажам и работа с возражениями.",
    ar: "اختر موديلاً لفتح بطاقته التدريبية الكاملة: الوصف، الألوان، الإطلالات الكاملة، نصائح البيع والتعامل مع الاعتراضات.",
    hy: "Ընտրեք մոդելը՝ դրա ամբողջական ուսումնական քարտը բացելու համար՝ նկարագրություն, գույներ, ընդհանուր կերպարներ, վաճառքի խորհուրդներ և առարկությունների հաղթահարում:",
    ka: "აირჩიეთ მოდელი მისი სრული სასწავლო ბარათის გასახსნელად: აღწერა, ფერები, სრული ლუქები, გაყიდვების რჩევები და შედავებთან მუშაობა.",
    uk: "Виберіть модель, щоб відкрити її повну навчальну картку: опис, кольори, тотал-луки, поради з продажу та роботу із запереченнями.",
    lv: "Izvēlieties modeli, lai atvērtu tā pilno apmācību karti: apraksts, krāsas, koptēli, pārdošanas padomi un darbs ar iebildumiem.",
    lt: "Pasirinkite modelį, kad atidarytumėte visą mokymo kortelę: aprašymas, spalvos, bendri įvaizdžiai, pardavimo patarimai ir prieštaravimų valdymas.",
    pl: "Wybierz model, aby otworzyć pełną kartę szkoleniową: opis, kolory, stylizacje total look, wskazówki sprzedażowe oraz zarządzanie obiekcjami.",
  },
  models: {
    en: "models",
    ru: "моделей",
    ar: "موديلات",
    hy: "մոդելներ",
    ka: "მოდელი",
    uk: "моделей",
    lv: "modeļi",
    lt: "modeliai",
    pl: "modeli",
  },
} as const;

const LanguageContext = createContext<Ctx>({
  lang: "en",
  isRtl: false,
  setLang: () => {},
  t: (k) => strings[k].en,
});

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>("en");

  useEffect(() => {
    const stored = localStorage.getItem(KEY) as Lang | null;
    if (stored && LANGUAGES.some((l) => l.code === stored)) {
      setLangState(stored);
    }
  }, []);

  useEffect(() => {
    const rtl = isRtlLang(lang);
    document.documentElement.dir = rtl ? "rtl" : "ltr";
    document.documentElement.lang = lang;
  }, [lang]);

  const setLang = useCallback((l: Lang) => {
    setLangState(l);
    localStorage.setItem(KEY, l);
  }, []);

  const t = useCallback(
    (k: keyof typeof strings) => {
      const table = strings[k] as Record<string, string>;
      return table[lang] || table.en || "";
    },
    [lang],
  );

  const isRtl = isRtlLang(lang);

  return (
    <LanguageContext.Provider value={{ lang, isRtl, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  return useContext(LanguageContext);
}
