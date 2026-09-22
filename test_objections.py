def parse_objections(raw):
    if not isinstance(raw, str) or not raw.strip():
        return []

    # 1. Sintassi [Obiezione] -> Risposta
    if "[" in raw and "]" in raw:
        out = []
        for block in re.split(r"\|\|", raw):
            block = block.strip().strip(",")
            if not block:
                continue
            m = re.match(r"^\s*\[(.+?)\]\s*->\s*(.*)$", block, flags=re.S)
            if m:
                out.append({"q": clean(m.group(1)), "a": clean(m.group(2))})
            else:
                out.append({"q": "", "a": clean(block)})
        if out:
            return out

    # 2. Formato con virgolette caporali «...»
    if "«" in raw:
        # Sostituiamo i refusi '---' prima della pulizia
        text_to_process = raw.replace("---", "города")

        # Puliamo il testo da immagini e URL, ma preserviamo la struttura
        cleaned = clean(text_to_process)
        cleaned = re.sub(
            r"^(Возражение|Заперечення|Iebildums|Obiekcja)?\s*(Стратегия\s+преодоления|Pārvarēšanas\s+stratēģija)?\s*",
            "",
            cleaned,
            flags=re.I,
        )

        out = []
        # Regex migliorata: cattura «Domanda/Inizio» e il testo successivo fino alla prossima « o fine stringa
        pattern = re.compile(r"«([^»]+)»\s*([^«]*)")
        matches = pattern.findall(cleaned)

        if matches:
            for q_raw, a_raw in matches:
                q = q_raw.strip(" \t\n\r,;«»")
                a = a_raw.strip(" \t\n\r,;«»")

                # Se la Strategy Word si trova ALL'INTERNO del blocco «...»
                strat_found = None
                strat_idx = -1
                for sw in STRATEGY_WORDS:
                    m = re.search(r"\b" + re.escape(sw) + r"\b", q)
                    if m:
                        if strat_idx == -1 or m.start() < strat_idx:
                            strat_idx = m.start()
                            strat_found = (m.start(), m.end(), sw)

                if strat_found:
                    actual_q = q[: strat_found[0]].strip(" \t\n\r,;«»")
                    actual_a = (q[strat_found[1] :] + " " + a).strip(" \t\n\r,;«»")
                    q, a = actual_q, actual_a

                # Formattazione e pulizia finale della risposta
                a = re.sub(r"^[,\s]+", "", a)
                a = re.sub(r"\s{2,}", " ", a)

                if q and a:
                    if not a.endswith("."):
                        a += "."
                    out.append({"q": q, "a": a})

            if out:
                return out

    # 3. Fallback per separatore pipe ||
    if "||" in raw:
        out = []
        for block in re.split(r"\|\|", raw):
            block = block.strip()
            if block:
                out.append({"q": "", "a": clean(block)})
        if out:
            return out

    # 4. Fallback blocco singolo
    return [{"q": "", "a": clean(raw)}]
