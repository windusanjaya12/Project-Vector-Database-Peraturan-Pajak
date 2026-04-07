# AI Tax Regulation Knowledge Base (Vector Database)

## Overview
Project ini merupakan project skripsi yang berjudul **knowledge base peraturan perpajakan Indonesia tahun 2024** berbasis **vector database** untuk mendukung pencarian informasi secara semantik. Dalam project ini digunakan **ChromaDB** sebagai vector database, **Sentence Transformer multilingual** sebagai model embedding, **Ollama qwen2.5:3b-instruct-q4_0** sebagai model LLM, dan **Streamlit** untuk antar muka chatbot.

Permasalahan utama dalam pencarian peraturan pajak adalah:
- Jumlah regulasi yang sangat banyak dan kompleks  
- Pencarian masih berbasis keyword  
- Sulit menemukan informasi yang benar-benar relevan  

Melalui project ini, dokumen peraturan pajak diubah menjadi representasi vektor menggunakan teknik **semantic embedding**, sehingga sistem dapat memahami **makna dan konteks**, bukan hanya kata kunci.

---

## Tujuan Project
- Membangun dataset peraturan pajak dalam bentuk vector embedding  
- Mengembangkan knowledge base untuk pencarian semantik  
- Mengimplementasikan chatbot AI sederhana berbasis vector database  
- Menjadi fondasi untuk sistem AI seperti RAG di masa depan  

---

## Cara Kerja Sistem

1. **Pengumpulan Data**  
   Mengambil dokumen peraturan pajak tahun 2024 dari situs resmi Direktorat Jenderal Pajak  

2. **Preprocessing**  
   - Ekstraksi teks dari PDF  
   - Pembersihan dan normalisasi teks  
   - Segmentasi menjadi pasal dan ayat  

3. **Embedding**  
   Mengubah teks menjadi vector menggunakan model sentence-transformers  

4. **Vector Database**  
   Menyimpan embedding ke dalam ChromaDB  

5. **Semantic Search & Chatbot**  
   - User menginput pertanyaan  
   - Sistem mencari konteks paling relevan dari vector database  
   - Chatbot menampilkan jawaban berdasarkan hasil pencarian tersebut  

---

## AI Chatbot
Sebagai implementasi dari knowledge base ini, dikembangkan **chatbot AI sederhana** yang mampu menjawab pertanyaan seputar peraturan pajak berdasarkan dataset vector yang telah dibuat.

Chatbot ini bekerja dengan pendekatan:
- Semantic search berbasis vector database  
- Mengambil informasi paling relevan dari dataset  
- Menyajikan jawaban berdasarkan konteks peraturan  

Contoh:
> Input: “Bagaimana langkah pelaporan pajak barang mewah?”  
> Output: Untuk melaporkan pajak atas barang merah, pihak penerima barang kena pajak harus menyampaikan permohonan SKB PPnBM secara elektronik melalui saluran pada laman Direktorat Jendral Pajak. Selain itu, pasal 205 ayat(3) dari Undang-Undang No. 78 Tahun 2024 juga menyebutkan bahwa wajib pajak yang tidak melaksanakan kewajiban tersebut akan ditagih oleh kepala Kantor Pelayanan Pajak tempat wajib pajak terdaftar dengan sanksi administratif sesuai peraturan peruntangan di bidang perpajakan.

---

## Features
- Semantic search berbasis embedding  
- Knowledge base peraturan pajak  
- Chatbot AI sederhana  
- Pencarian berbasis konteks (bukan keyword)  
- Dataset regulasi pajak tahun 2024  

---

## Requirements
chromadb
pdfplumber
tqdm
sentence-transformers
matplotlib