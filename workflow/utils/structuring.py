import re


def detect_unclear_sections(text):
    unclear = []
    indicators = [
        "[OCR_FAILED",
        "illegible",
        "unclear",
        "not readable",
        "???",
    ]

    for line in text.splitlines():
        if any(i.lower() in line.lower() for i in indicators):
            unclear.append(line[:200])

    return unclear


def extract_after_keywords(text, keywords):
    found = []

    for keyword in keywords:
        pattern = rf"{keyword}\s*[:\-]\s*(.+)"
        matches = re.findall(pattern, text, flags=re.I)
        found.extend([m.strip()[:120] for m in matches])

    return list(set(found))


def extract_structured_data(text):
    parties = extract_after_keywords(
        text,
        ["Plaintiff", "Defendant", "Client", "Seller", "Buyer"]
    )

    dates = re.findall(
        r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b",
        text
    )

    money = re.findall(
        r"(?:USD|BDT|Tk\.?|৳|\$)\s?\d[\d,]*(?:\.\d+)?",
        text,
        flags=re.I
    )

    return {
        "possible_parties": parties,
        "dates": list(set(dates)),
        "monetary_amounts": list(set(money)),
        "unclear_sections": detect_unclear_sections(text),
    }