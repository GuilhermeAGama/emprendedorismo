import chromadb


client = chromadb.PersistentClient(
    path="./vector_database"
)


collection = client.get_or_create_collection(
    name="respostas_avaliadas",
    metadata={
        "hnsw:space": "cosine"
    }
)