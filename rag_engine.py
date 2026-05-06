import ollama
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="soporte_tecnico")

def buscar_contexto(pregunta, top_k=3):

    pregunta_embedding = ollama.embeddings(
        model="nomic-embed-text",
        prompt=pregunta
    )["embedding"]

    resultados = collection.query(
        query_embeddings=[pregunta_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    documentos = resultados["documents"][0]
    metadatas = resultados["metadatas"][0]
    distancias = resultados["distances"][0]

    contexto = ""
    evidencia = ""

    for i in range(len(documentos)):
        contexto += f"\n[Fuente {i+1} - {metadatas[i]['source']}]\n{documentos[i]}\n"
        evidencia += f"Resultado {i+1} | Fuente documental recuperada: {metadatas[i]['source']}\n"

    return contexto, evidencia