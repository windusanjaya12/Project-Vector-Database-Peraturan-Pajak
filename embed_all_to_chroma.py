import json
import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = "./chroma_data_final"
COLLECTION_NAME = "peraturan_pajak_final"
JSON_PATH = "./output_chunks/ALL_REGULASI.json"

# ================================
# EMBEDDING FUNCTION
# ================================
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="intfloat/multilingual-e5-large"
)

# ================================
# INIT CHROMA (DB BARU)
# ================================
client = chromadb.PersistentClient(path=CHROMA_PATH)

col = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_func,
    metadata={"source": "regulasi_pajak_2024"}
)

# ================================
# LOAD & DEDUP JSON
# ================================
with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

unique = {}
for d in data:
    unique[d["id"]] = d   # overwrite duplicate safely

clean_data = list(unique.values())

print(f" Chunk awal   : {len(data)}")
print(f" Setelah dedup: {len(clean_data)}")

# ================================
# PREPARE INSERT
# ================================
ids = [d["id"] for d in clean_data]
docs = [d["text"] for d in clean_data]
metas = [d["metadata"] for d in clean_data]

# ================================
# INSERT
# ================================
print("Mulai embedding...")
BATCH_SIZE = 1000  # aman, ringan, stabil

for i in range(0, len(ids), BATCH_SIZE):
    col.add(
        ids=ids[i:i+BATCH_SIZE],
        documents=docs[i:i+BATCH_SIZE],
        metadatas=metas[i:i+BATCH_SIZE],
    )
    print(f"Insert batch {i} - {min(i+BATCH_SIZE, len(ids))}")

print("SELESAI")
print("Total vector:", len(ids))
