import re
from typing import List, Dict

PASAL_PATTERN = re.compile(
    r"(?m)^(Pasal\s+\d+[A-Z]?)\b"
)

def parse_pasal_final(text: str) -> List[Dict]:
    """
    Parser FINAL toleran untuk regulasi Indonesia.
    - Pasal boleh diikuti judul/paragraf
    - Semua isi digabung sampai Pasal berikutnya
    """

    matches = list(PASAL_PATTERN.finditer(text))
    pasal_blocks = []

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        pasal = match.group(1)
        isi = text[start + len(pasal):end].strip()

        # validasi minimal isi
        if len(isi.split()) < 20:
            continue

        pasal_blocks.append({
            "jenis_konten": "pasal",
            "pasal": pasal,
            "isi": isi
        })
    return pasal_blocks
