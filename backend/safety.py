BLOCKED_KEYWORDS = [
    "duty",
    "customs duty",
    "calculate",
    "hs code",
    "classify",
    "legal advice",
    "should i",
    "can i export",
    "clear my shipment"
]

def is_safe_query(query: str):
    q = query.lower()
    for word in BLOCKED_KEYWORDS:
        if word in q:
            return False
    return True

def safety_message():
    return (
        "This system cannot calculate duties, classify HS codes, or provide "
        "personalized legal or customs advice. It can only explain public "
        "government procedures and policies."
    )
