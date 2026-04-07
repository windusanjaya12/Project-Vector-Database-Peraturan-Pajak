import re
import streamlit as st
import chromadb
from langchain_community.llms import Ollama

# =========================
# KONFIGURASI
# =========================
CHROMA_PATH = "./chroma_data_final"
COLLECTION_NAME = "peraturan_pajak_final"
LLM_MODEL = "qwen2.5:3b-instruct-q4_0"

st.set_page_config(page_title="Chatbot Regulasi Pajak", layout="wide")
st.title("📚 Chatbot Regulasi Pajak (Semantic Search)")

query = st.text_input("Masukkan pertanyaan tentang peraturan pajak:")

# =========================
# INIT CHROMA ( TANPA embedding_function)
# =========================
client = chromadb.PersistentClient(path="chroma_data_final")
collection = client.get_collection(name="peraturan_pajak_final")

# =========================
# INIT LLM
# =========================
llm = Ollama(model=LLM_MODEL, temperature=0)

# =========================
# UTIL: CEK APAKAH USER MENYEBUT REGULASI
# =========================
def user_mentions_regulation(text: str) -> bool:
    pattern = r"\b(PMK|PER|PP|PERPRES|KM)\b|\b20\d{2}\b"
    return bool(re.search(pattern, text.upper()))

# =========================
# QUERY PIPELINE
# =========================
if query:
    with st.spinner(" Mencari regulasi..."):
        results = collection.query(
            query_texts=[query],
            n_results=5
        )
        docs = results["documents"][0]
        metas = results["metadatas"][0]

    # =========================
    # BUILD CONTEXT (UNTUK LLM)
    # =========================
    context_blocks = []
    for d, m in zip(docs, metas):
        block = (
            f"Jenis: {m.get('jenis_peraturan')}\n"
            f"Nomor: {m.get('nomor_tahun')}\n"
            f"Pasal: {m.get('pasal')}\n"
            f"Ayat: {m.get('ayat')}\n"
            f"Isi: {d}"
        )
        context_blocks.append(block)

    context = "\n\n---\n\n".join(context_blocks)

    # =========================
    # PROMPT (AMAN SECARA HUKUM)
    # =========================
    if user_mentions_regulation(query):
        prompt = f"""
Anda adalah asisten hukum pajak Indonesia.

Jawablah secara:
- faktual
- berbasis teks regulasi
- sebutkan pasal jika memang relevan

KONTEKS REGULASI:
{context}

PERTANYAAN:
{query}

JAWABAN:
"""
    else:
        prompt = f"""
Anda adalah asisten analisis regulasi perpajakan Indonesia berbasis database.

BATASAN WAJIB:
1. Jawaban HANYA boleh berdasarkan KONTEKS yang diberikan.
2. DILARANG menggunakan pengetahuan di luar konteks.
3. Jika informasi TIDAK ditemukan secara eksplisit, katakan dengan jelas:
   "Tidak ditemukan pengaturan eksplisit dalam regulasi yang tersedia."
4. JANGAN menyebutkan peraturan yang tidak muncul di konteks.
5. JANGAN mengasumsikan jenis peraturan jika tidak disebutkan.

FORMAT JAWABAN:
- Jawaban singkat dan langsung
- Jika ada dasar hukum, sebutkan:
  Jenis Peraturan – Nomor/Tahun – Pasal – Ayat
- Jika tidak ada, cukup satu paragraf penjelasan defensif

KONTEKS REGULASI:
{context}

PERTANYAAN:
{query}

JAWABAN:
"""

    # =========================
    # GENERATE ANSWER
    # =========================
    with st.spinner("🧠 Menyusun jawaban..."):
        answer = llm.invoke(prompt)

    st.markdown("### 📝 Jawaban")
    st.write(answer)

    # =========================
    # SUMBER (HANYA JIKA USER MENYEBUT)
    # =========================
    if user_mentions_regulation(query):
        with st.expander("📄 Sumber Regulasi"):
            for m in metas:
                st.write(
                    f"- {m.get('jenis_peraturan')} {m.get('nomor_tahun')} | "
                    f"{m.get('pasal')} {m.get('ayat')}"
                )
