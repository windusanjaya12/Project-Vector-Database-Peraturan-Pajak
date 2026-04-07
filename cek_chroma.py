import chromadb

client = chromadb.PersistentClient(path="./chroma_data_final")

print("📦 Collection yang tersedia:")
print(client.list_collections())
