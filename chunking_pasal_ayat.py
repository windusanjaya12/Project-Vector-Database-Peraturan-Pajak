import re
import hashlib

def make_id(text: str):
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:8]

def split_ayat(text: str):
    # Pisahkan berdasarkan (1), (2), dst
    parts = re.split(r"\n?\((\d+)\)\s*", text)
    ayats = []
    for i in range(1, len(parts), 2):
        nomor = parts[i]
        isi = parts[i+1].strip()
        if len(isi) > 20:
            ayats.append((nomor, isi))
    return ayats

def chunk_pasal_to_ayat(pasal_data, jenis, nomor_tahun, judul):
    chunks = []
    pasal = pasal_data["pasal"]
    isi = pasal_data["isi"]

    ayats = split_ayat(isi)

    for idx, (no, teks) in enumerate(ayats):
        text_norm = teks.lower()
        mode = "luring" if "luring" in text_norm else "elektronik"

        chunk_text = f"{pasal} ayat ({no})\n{teks}"

        chunk_id = f"{jenis}_{nomor_tahun}_{pasal}_ayat_{no}_{make_id(chunk_text)}"

        chunks.append({
            "id": chunk_id,
            "text": chunk_text,
            "metadata": {
                "jenis": jenis,
                "nomor_tahun": nomor_tahun,
                "judul": judul,
                "pasal": pasal,
                "ayat": f"({no})",
                "mode_pengajuan": mode
            }
        })

    return chunks