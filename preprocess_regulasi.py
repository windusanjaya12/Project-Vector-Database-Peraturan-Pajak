import fitz
from legal_cleaner import clean_legal_text
from parse_pasal_final import parse_pasal_final

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    all_lines = []

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b["type"] != 0:
                continue
            for line in b["lines"]:
                line_text = " ".join(span["text"] for span in line["spans"])
                if line_text.strip():
                    all_lines.append(line_text)

    return "\n".join(all_lines)


def process_regulation(pdf_path):
    raw = extract_text(pdf_path)
    clean = clean_legal_text(raw)

    pasal_chunks = parse_pasal_final(clean)

    return pasal_chunks, None


if __name__ == "__main__":
    pdf_path = "data_pdf/LAMPIRAN PMK 28 TAHUN 2024.pdf" # ganti sesuai file PDF Anda

    pasal, lampiran = process_regulation(pdf_path)

    print("Jumlah pasal:", len(pasal))
    print("\nContoh 1 pasal:\n")
    print(pasal[0])

    if lampiran:
        print("\nLampiran terdeteksi (potongan):\n")
        print(lampiran[:500])
