def format_enterprise_answer(query, answer, meta_list):

    NOINFO = "No relevant information found in the provided documents."

    # 1️⃣ If no info → return simple output
    if answer.strip() == NOINFO:
        return NOINFO, []

    # 2️⃣ Flatten metadata (avoid list/dict crashes)
    normalized = []
    for m in meta_list:
        if isinstance(m, dict):
            normalized.append(m)
        elif isinstance(m, list):
            for x in m:
                if isinstance(x, dict):
                    normalized.append(x)

    # 3️⃣ Remove wrong-direction terms
    if "export" in query.lower():
        banned_terms = ["bill of entry", "import declaration"]
        for b in banned_terms:
            answer = answer.replace(b, "")
    if "import" in query.lower():
        banned_terms = ["shipping bill", "export declaration"]
        for b in banned_terms:
            answer = answer.replace(b, "")

    # Clean extra spaces
    answer = " ".join(answer.split())

    # 4️⃣ Deduplicate metadata
    unique = []
    seen = set()
    for m in normalized:
        key = (m.get("file_name"), m.get("category"))
        if key not in seen:
            seen.add(key)
            unique.append({"file_name": key[0], "category": key[1]})

    return answer, unique
