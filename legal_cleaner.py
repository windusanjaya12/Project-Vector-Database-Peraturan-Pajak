import re

def clean_legal_text(text: str) -> str:
    # hapus karakter aneh & ikon
    text = re.sub(r"[\uf000-\uf0ff]", "", text)

    # hapus noise navigasi
    blacklist_patterns = [
        r"ID\s*\(/id\).*",
        r"EN\s*\(/en/.*\)",
        r"MENU",
        r"facebook|twitter|whatsapp|telegram",
        r"\(/id\)",
        r"\(/en/.*\)",
    ]

    for p in blacklist_patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE)

    # rapikan spasi
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)

    return text.strip()
