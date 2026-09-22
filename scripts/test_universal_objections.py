#!/usr/bin/env python3
"""
Universal multilingual objection parser.
Handles all languages with proper Unicode word boundary detection.
"""

import re
import csv
import json

# Encoding cleanup replacements
CHAR_FIXES = [
    ("»™s", "'s"),
    ("»™", "'"),
    ("»”", "—"),
    ("»\x9d", "»"),
    ("\x9d", ""),
    ("â€”", "—"),
    ("â€™", "'"),
    ("â€œ", "“"),
    ("â€", "”"),
    ("---", "—"),
    ("Ã©", "é"),
    ("Ã¨", "è"),
    ("Ã", "à"),
]

MARKDOWN_IMAGE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
WORD_IMAGE_DIRECTIVE = re.compile(r"\.?\s*!\[([^\]]*)\]\([^)]+\)\s*\{[^}]*\}")
PAREN_URL = re.compile(r"\(\s*(?:https?://)[^()]*(?:\([^()]*\)[^()]*)*\)")
BARE_URL = re.compile(r"https?://\S+")

STRATEGY_WORDS_BY_LANG = {
    "ru": [
        "Поясните", "Укажите", "Предложите", "Продемонстрируйте", "Рекомендуйте",
        "Объясните", "Обратите внимание", "Покажите", "Подчеркните", "Напомните",
        "Заверьте", "Сделайте акцент", "Расскажите", "Акцентируйте", "Посоветуйте",
        "Сделайте упор", "Обоснуйте",
    ],
    "en": [
        "Explain that", "Explain", "Clarify that", "Clarify", "Showcase", "Show",
        "Remind the client that", "Remind the client", "Remind", "Suggest trying",
        "Suggest completing", "Suggest pairing", "Suggest", "Recommend completing",
        "Recommend trying", "Recommend pairing", "Recommend", "Point out the",
        "Point out", "Point to the", "Point to", "On the contrary", "Highlight the",
        "Highlight that", "Highlight", "Demonstrate", "Emphasise the", "Emphasise",
        "Emphasize the", "Emphasize", "Advise", "Assure the client", "Assure",
        "Note that", "Direct attention", "Draw attention",
    ],
    "pl": [
        "Wyjaśnij", "Proszę wyjaśnić", "Zwróć uwagę", "Podkreśl", "Pokaż", "Zaproponuj",
        "Przypomnij", "Zapewnij", "Doradź", "Zademonstruj", "Wskaż",
    ],
    "uk": [
        "Поясніть", "Зверніть увагу", "Підкресліть", "Покажіть", "Запропонуйте",
        "Нагадайте", "Запевніть", "Порадьте", "Продемонструйте", "Вкажіть",
    ],
    "lv": [
        "Izskaidrojiet", "Pievērsiet uzmanību", "Uzsveriet", "Parādiet", "Piedāvājiet",
        "Atgādiniet", "Iesakiet", "Demonstrējiet", "Nodemonstrējiet", "Norādiet", "Paskaidrojiet", "Izceliet",
    ],
    "lt": [
        "Paaiškinkite", "Atkreipkite dėmesį", "Pabrėžkite", "Parodykite", "Pasiūlykite",
        "Prisiminkite", "Priminkite", "Patarkite", "Pademonstruokite", "Nurodykite",
    ],
    "ka": [
        "განუმარტეთ", "განმარტეთ", "ყურადღება გაამახვილეთ", "ხაზი გაუსვით", "აჩვენეთ", "შესთავაზეთ",
        "შეახსენეთ", "ურჩიეთ", "წარმოაჩინეთ", "მიუთითეთ", "გირჩიეთ",
    ],
    "hy": [
        "Պարզաբանեք", "Ուշադրություն դարձրեք", "Ընդգծեք", "Ցույց տվեք", "Առաջարկեք",
        "Հիշեցրեք", "Վստահեցրեք", "Խորհուրդ տվեք", "Ցուցադրեք", "Նշեք",
    ],
    "ar": [
        "اشرحي", "اشرح", "وضحي", "وضح", "لفت الانتباه", "أكدي", "أكد", "أظهري", "أظهر",
        "اقترحي", "اقترح", "ذكّري", "ذكّر", "انصحي", "انصح", "استعرضي", "استعرض",
        "أشيري", "أشر", "نوصي", "نوصي بتكملة",
    ],
}

ALL_STRATEGY_WORDS = []
for words in STRATEGY_WORDS_BY_LANG.values():
    ALL_STRATEGY_WORDS.extend(words)
ALL_STRATEGY_WORDS = sorted(set(ALL_STRATEGY_WORDS), key=len, reverse=True)


def clean_objection_text(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""
    t = text
    for old, new in CHAR_FIXES:
        t = t.replace(old, new)
    t = PAREN_URL.sub("", t)
    t = BARE_URL.sub("", t)
    t = WORD_IMAGE_DIRECTIVE.sub("", t)
    t = MARKDOWN_IMAGE.sub("", t)
    t = re.sub(r"\(\s*(nan|Данные отсутствуют[^)]*|URL non disponibile|Data not available[^)]*)\s*\)", "", t, flags=re.I)
    t = re.sub(r"\bData not available in official sources\b", "", t, flags=re.I)
    t = re.sub(r"\bData not available\b", "", t, flags=re.I)
    t = re.sub(r"\bДанные отсутствуют в официальных источниках\b", "", t, flags=re.I)
    t = re.sub(r"\bმონაცემები არ არსებობს ოფიციალურ წყაროებში\b", "", t, flags=re.I)
    t = re.sub(r"\bმონაცემები არ არსებობს\b", "", t, flags=re.I)
    t = re.sub(r"\bՏվյալները բացակայում են պաշտոնական աղբյուրներում\b", "", t, flags=re.I)
    t = re.sub(r"\bՏվյալները բացակայում են\b", "", t, flags=re.I)
    t = re.sub(r"\bDati nav pieejami oficiālajos avotos\b", "", t, flags=re.I)
    t = re.sub(r"\bDati nav pieejami\b", "", t, flags=re.I)
    t = re.sub(r"\bDuomenų nėra oficialiuose šaltiniuose\b", "", t, flags=re.I)
    t = re.sub(r"\bDuomenų nėra\b", "", t, flags=re.I)
    t = re.sub(r"\bBrak danych w oficjalnych źródłach\b", "", t, flags=re.I)
    t = re.sub(r"\bBrak danych\b", "", t, flags=re.I)
    t = re.sub(r"\bДані відсутні в офіційних джерелах\b", "", t, flags=re.I)
    t = re.sub(r"\bДані відсутні\b", "", t, flags=re.I)
    t = re.sub(r"\s+([,.;:!?،؛])", r"\1", t)
    t = re.sub(r"([,.;:!?،؛])\s*([,.;:!?،؛])+", r"\1", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip(" ,;")


def clean_str(s: str) -> str:
    if not s:
        return ""
    t = s.strip(" \t\n\r,;«»“”\"':،؛")
    t = re.sub(r"^(?:Objection\s*\d*\s*[:\-]|Response\s*[:\-]|Возражение\s*[:\-]|Ответ\s*[:\-]|الاعتراض\s*[:\-]|الرد\s*[:\-])\s*", "", t, flags=re.I)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip(" \t\n\r,;«»“”\"':،؛")


def parse_bracket_format(text: str) -> list[dict]:
    out = []
    blocks = re.split(r"\|\|", text) if "||" in text else [text]
    for block in blocks:
        block = block.strip().strip(",")
        if not block:
            continue
        matches = list(re.finditer(r"\[\s*(.+?)\s*\]\s*(?:->|–>|→|:)\s*", block, flags=re.S))
        if matches:
            for i, m in enumerate(matches):
                q = m.group(1).strip()
                start_ans = m.end()
                end_ans = matches[i + 1].start() if i + 1 < len(matches) else len(block)
                a = block[start_ans:end_ans].strip(" \t\n\r,;«»“”\"'")
                if q and a and not any(neg in q.lower() for neg in ["отсутствуют", "not available", "nav pieejami", "nėra", "brak danych", "відсутні", "არ არსებობს", "բացակայում"]):
                    out.append({"q": clean_str(q), "a": clean_str(a)})
        else:
            m = re.match(r"^\s*\[\s*(.+?)\s*\]\s*(?:->|–>|→|:)\s*(.*)$", block, flags=re.S)
            if m:
                q = m.group(1).strip()
                a = m.group(2).strip(" \t\n\r,;«»“”\"'")
                if q and a and not any(neg in q.lower() for neg in ["отсутствуют", "not available", "nav pieejami", "nėra", "brak danych", "відсутні", "არ არსებობს", "բացակայում"]):
                    out.append({"q": clean_str(q), "a": clean_str(a)})
    return out


def parse_keyword_obj_resp(text: str, lang: str = "en") -> list[dict]:
    out = []
    obj_pattern = re.compile(
        r"(?:(?:^|\s+)(?:Objection\s*\d*\s*:|Objection\s+Overcoming\s+Strategy\s*:?|الاعتراض\s*:|Առարկություն\s*[՝:]|Iebildums\s*:|Prieštaravimas\s*:|Zastrzeżenie\s*:|Obiekcja\s*:|Заперечення\s*:|Возражение\s*:))",
        re.I
    )
    resp_pattern = re.compile(
        r"(?:Response\s*:|Стратегия\s*(?:преодоления|суперamento)?\s*:|استراتيجية\s*(?:التجاوز)?\s*:|Ռազմավարություն\s*[՝:]|Հաղթահարման\s*ռազմավարություն\s*[՝:]|Stratēģija\s*(?:pārvarēšanai|superamento)?\s*:|Pārvarēšanas\s*stratēģija\s*:|Strategija\s*(?:įveikti|superamento)?\s*:|Įveikimo\s*stratēģija\s*:|Strategia\s*(?:przezwyciężenia|superamento)?\s*:|Стратегія\s*(?:подолання|суперamento)?\s*:)",
        re.I
    )

    splits = list(obj_pattern.finditer(text))
    if len(splits) >= 1:
        for i, m in enumerate(splits):
            start = m.end()
            end = splits[i + 1].start() if i + 1 < len(splits) else len(text)
            chunk = text[start:end].strip()
            if not chunk:
                continue

            resp_m = resp_pattern.search(chunk)
            if resp_m:
                q_part = chunk[:resp_m.start()].strip(" \t\n\r,;«»“”\"':،؛")
                a_part = chunk[resp_m.end():].strip(" \t\n\r,;«»“”\"':،؛")
                if q_part and a_part:
                    out.append({"q": clean_str(q_part), "a": clean_str(a_part)})
            else:
                guill_m = re.match(r"^[\s«„“\"]+(.+?)[\s»“”\"]+(.*)$", chunk, re.S)
                if guill_m:
                    q_part = guill_m.group(1).strip(" \t\n\r,;«»“”\"':،؛")
                    a_part = guill_m.group(2).strip(" \t\n\r,;«»“”\"':،؛")
                    if q_part and a_part:
                        out.append({"q": clean_str(q_part), "a": clean_str(a_part)})

    return out


def make_word_regex(word: str) -> re.Pattern:
    # Safe boundary pattern for all Unicode characters
    return re.compile(r"(?:(?<=[\s«„“\"'(\[{])|^)" + re.escape(word) + r"(?:(?=[\s»”\"')\]}:,.;!?،؛])|$)", re.I)


def parse_strategy_sequence(text: str, lang: str = "ru") -> list[dict]:
    cleaned = re.sub(
        r"^(?:Возражение\s+Стратегия(?:\s+[^\s«„“\"\[]+)?\s*|Objection\s+Overcoming\s+Strategy\s*|الاعتراض\s+استراتيجية(?:\s+[^\s«„“\"\[]+)?\s*|გაპროტესტება\s+სტრატეგია(?:\s+[^\s«„“\"\[]+)?\s*|Առարկություն\s+[^\s«„“\"\[]+\s*|Iebildums\s+Stratēģija(?:\s+[^\s«„“\"\[]+)?\s*|Iebildums\s+Pārvarēšanas\s+stratēģija\s*|Prieštaravimas\s+Strategija(?:\s+[^\s«„“\"\[]+)?\s*|Prieštaravimas\s+Įveikimo\s+stratēģija\s*|Obiekcja\s+Strategia(?:\s+[^\s«„“\"\[]+)?\s*|Obiekcja\s+Strategia\s+przezwyciężenia\s*|Заперечення\s+Стратегія(?:\s+[^\s«„“\"\[]+)?\s*|Заперечення\s+Стратегія\s+подолання\s*)",
        "",
        text,
        flags=re.I
    ).strip()

    strategy_words = STRATEGY_WORDS_BY_LANG.get(lang, []) or ALL_STRATEGY_WORDS

    # 1. Clean split by «...» or quotes
    # If text contains pairs of quotes like «Question» Answer «Question 2» Answer 2
    quote_matches = list(re.finditer(r"[«„“\"]([^»”\"]+)[»”\"]", cleaned))
    if len(quote_matches) >= 1:
        out = []
        for i, qm in enumerate(quote_matches):
            inside = qm.group(1).strip()
            # Check if strategy word is inside the quote or after the quote
            strat_found = None
            for sw in strategy_words:
                m = make_word_regex(sw).search(inside)
                if m:
                    if strat_found is None or m.start() < strat_found[0]:
                        strat_found = (m.start(), m.end(), sw, "inside")

            next_quote_start = quote_matches[i + 1].start() if i + 1 < len(quote_matches) else len(cleaned)
            outside_after = cleaned[qm.end():next_quote_start].strip()

            if not strat_found:
                # Check if strategy word is outside
                for sw in strategy_words:
                    m = make_word_regex(sw).search(outside_after)
                    if m:
                        if strat_found is None or m.start() < strat_found[0]:
                            strat_found = (m.start(), m.end(), sw, "outside")

            if strat_found and strat_found[3] == "inside":
                q = inside[:strat_found[0]].strip()
                ans_inside = inside[strat_found[0]:].strip()
                a = (ans_inside + " " + outside_after).strip()
            else:
                q = inside
                a = outside_after

            q_clean = clean_str(q)
            a_clean = clean_str(a)
            if q_clean and a_clean:
                if not a_clean.endswith((".", "!", "?", "…")):
                    a_clean += "."
                out.append({"q": q_clean, "a": a_clean})
        if out:
            return out

    # 2. No quotes: search strategy words in raw text
    matches = []
    for sw in strategy_words:
        for m in make_word_regex(sw).finditer(cleaned):
            matches.append((m.start(), m.end(), m.group(0)))

    matches.sort(key=lambda x: x[0])
    filtered_matches = []
    last_end = 0
    for start, end, word in matches:
        if start >= last_end:
            filtered_matches.append((start, end, word))
            last_end = end

    if len(filtered_matches) >= 1:
        out = []
        for i, (strat_start, strat_end, sw) in enumerate(filtered_matches):
            prev_answer_end = filtered_matches[i - 1][1] if i > 0 else 0
            chunk_before = cleaned[prev_answer_end:strat_start].strip()

            if i == 0:
                q = chunk_before
            else:
                sentence_splits = list(re.finditer(r"[\.!?،؛]\s+([^\s\d])", chunk_before))
                if sentence_splits:
                    last_split = sentence_splits[-1]
                    q = chunk_before[last_split.start() + 1:].strip()
                    if out:
                        prev_ans_extra = chunk_before[:last_split.start() + 1].strip()
                        out[-1]["a"] = (out[-1]["a"] + " " + prev_ans_extra).strip()
                else:
                    words = chunk_before.split()
                    if len(words) > 6:
                        q = " ".join(words[-6:]).strip()
                    else:
                        q = chunk_before.strip()

            next_strat_start = filtered_matches[i + 1][0] if i + 1 < len(filtered_matches) else len(cleaned)
            a_chunk = cleaned[strat_start:next_strat_start].strip()

            if i + 1 < len(filtered_matches):
                sentence_splits = list(re.finditer(r"[\.!?،؛]\s+([^\s\d])", a_chunk))
                if sentence_splits:
                    last_split = sentence_splits[-1]
                    a = a_chunk[:last_split.start() + 1].strip()
                else:
                    a = a_chunk.strip()
            else:
                a = a_chunk.strip()

            q_clean = clean_str(q)
            a_clean = clean_str(a)
            if q_clean and a_clean:
                if not a_clean.endswith((".", "!", "?", "…")):
                    a_clean += "."
                out.append({"q": q_clean, "a": a_clean})

        if out:
            return out

    return []


def parse_universal_objections(raw_text: str, lang: str = "en") -> list[dict]:
    if not raw_text or not isinstance(raw_text, str):
        return []

    cleaned = clean_objection_text(raw_text)
    if not cleaned:
        return []

    # 1. Bracket format
    if "[" in cleaned and "]" in cleaned and any(arrow in cleaned for arrow in ["->", "–>", "→", ":"]):
        res = parse_bracket_format(cleaned)
        if res:
            return res

    # 2. Objection: ... Response: ... format
    res = parse_keyword_obj_resp(cleaned, lang)
    if res:
        return res

    # 3. Strategy sequence
    res = parse_strategy_sequence(cleaned, lang)
    if res:
        return res

    if lang != "ru":
        res = parse_strategy_sequence(cleaned, "ru")
        if res:
            return res

    return []
