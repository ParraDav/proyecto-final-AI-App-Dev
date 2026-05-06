import ollama
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="soporte_tecnico")

def buscar_contexto(pregunta, top_k=4):

    pregunta_embedding = ollama.embeddings(
        model="nomic-embed-text",
        prompt=pregunta
    )["embedding"]

    resultados = collection.query(
        query_embeddings=[pregunta_embedding],
        n_results=top_k
    )

    documentos = resultados["documents"][0]
    fuentes = resultados["metadatas"][0]

    contexto = ""
    for i, doc in enumerate(documentos):
        contexto += f"\n[Fuente {i+1} - {fuentes[i]['source']}]\n{doc}\n"

    return contexto