# ================================
# IMPORT LIBRARY
# ================================
import os          # Untuk operasi file & folder
import json        # Untuk menyimpan hasil preprocessing ke format JSON
import re          # Untuk pencocokan pola (regex)

# Import modul internal preprocessing
from preprocess_regulasi import process_regulation
from chunking_pasal_ayat import chunk_pasal_to_ayat


# ================================
# KONFIGURASI DIREKTORIk
# ================================
# Folder berisi dokumen PDF peraturan pajak
DATA_PDF = "data_pdf"

# Folder output hasil chunking (JSON)
OUT = "output_chunks"

# Membuat folder output jika belum ada
os.makedirs(OUT, exist_ok=True)


# ================================
# FUNGSI IDENTIFIKASI JENIS PERATURAN
# ================================
def infer_jenis(fname: str):
    """
    Menentukan jenis peraturan berdasarkan nama file PDF.
    Contoh:
    - PMK → Peraturan Menteri Keuangan
    - PP → Peraturan Pemerintah
    - PER → Peraturan Dirjen
    """
    fname = fname.upper()

    if "PMK" in fname:
        return "PMK"
    if "PERPRES" in fname:
        return "PERPRES"
    if "PER " in fname or "PER_" in fname:
        return "PER"
    if "PP " in fname or "PP_" in fname:
        return "PP"
    if "KM" in fname:
        return "KM"

    return "UNKNOWN"


# ================================
# FUNGSI IDENTIFIKASI NOMOR & TAHUN
# ================================
def infer_nomor_tahun(fname: str):
    """
    Mengambil nomor dan tahun peraturan dari nama file
    Contoh:
    'PMK 78 Tahun 2024.pdf' → 78_2024
    """
    m = re.search(r"(\d+).*?(20\d{2})", fname)
    if m:
        return f"{m.group(1)}_{m.group(2)}"

    return "UNKNOWN"


# ================================
# PENAMPUNG SELURUH CHUNK REGULASI
# ================================
all_chunks = []


# ================================
# PROSES UTAMA PREPROCESSING
# ================================
# Loop untuk membaca seluruh file PDF dalam folder data_pdf
for f in os.listdir(DATA_PDF):

    # Hanya memproses file PDF
    if not f.lower().endswith(".pdf"):
        continue

    # Path lengkap file PDF
    path = os.path.join(DATA_PDF, f)

    # Infer metadata peraturan dari nama file
    jenis = infer_jenis(f)
    nomor_tahun = infer_nomor_tahun(f)

    print(f"▶ Memproses: {f} | {jenis} | {nomor_tahun}")

    # ================================
    # EKSTRAKSI & PEMBERSIHAN TEKS
    # ================================
    # process_regulation:
    # - Ekstraksi teks PDF
    # - Cleaning teks hukum
    # - Segmentasi menjadi pasal
    pasal_list, _ = process_regulation(path)

    # ================================
    # CHUNKING PASAL → AYAT
    # ================================
    for p in pasal_list:

        # Memecah setiap pasal menjadi ayat
        # serta menambahkan metadata hukum
        ayat_chunks = chunk_pasal_to_ayat(
            pasal_data=p,
            jenis=jenis,
            nomor_tahun=nomor_tahun,
            judul=f.replace(".pdf", "")
        )

        # Menyimpan seluruh chunk ayat
        all_chunks.extend(ayat_chunks)


# ================================
# PENYIMPANAN KE FORMAT JSON
# ================================
with open(
    os.path.join(OUT, "ALL_REGULASI.json"),
    "w",
    encoding="utf-8"
) as w:
    json.dump(all_chunks, w, ensure_ascii=False, indent=2)


# ================================
# INFORMASI AKHIR PROSES
# ================================
print(" SELESAI")
print("Total chunk:", len(all_chunks))
