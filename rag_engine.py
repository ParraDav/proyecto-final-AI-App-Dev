import ollama
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="soporte_tecnico")

def buscar_contexto(pregunta, top_k=6):

    pregunta_embedding = ollama.embeddings(
        model="nomic-embed-text",
        prompt=pregunta
    )["embedding"]

    resultados = collection.query(
        query_embeddings=[pregunta_embedding],
        n_results=top_k,
        include=["documents", "metadatas"]
    )

    documentos = resultados["documents"][0]
    metadatas = resultados["metadatas"][0]

    contexto = ""
    evidencia = ""
    fuentes_usadas = set()
    contador = 1

    for i in range(len(documentos)):
        fuente = metadatas[i]["source"]

        if fuente not in fuentes_usadas:
            contexto += f"\n[Fuente {contador} - {fuente}]\n{documentos[i]}\n"
            evidencia += f"Resultado {contador} | Fuente documental recuperada: {fuente}\n"
            fuentes_usadas.add(fuente)
            contador += 1

        if contador > 3:
            break

    return contexto, evidencia