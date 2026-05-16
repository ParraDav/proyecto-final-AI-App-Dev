import ollama
import chromadb

# =====================================================
# CONEXIÓN CHROMADB
# =====================================================

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection(
    name="soporte_tecnico"
)

# =====================================================
# BÚSQUEDA SEMÁNTICA
# =====================================================

def buscar_contexto(pregunta, top_k=6):

    # ==========================================
    # EMBEDDING DE PREGUNTA
    # ==========================================

    pregunta_embedding = ollama.embeddings(
        model="nomic-embed-text",
        prompt=pregunta
    )["embedding"]

    # ==========================================
    # CONSULTA VECTORIAL
    # ==========================================

    resultados = collection.query(
        query_embeddings=[pregunta_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    documentos = resultados["documents"][0]
    metadatas = resultados["metadatas"][0]
    distancias = resultados["distances"][0]

    contexto = ""
    evidencia = ""

    fuentes = []

    fuentes_usadas = set()

    contador = 1

    # ==========================================
    # FILTRADO DE RESULTADOS
    # ==========================================

    for i in range(len(documentos)):

        # Filtrar resultados poco relevantes
        #quedará comentado debido a la poca documentación en este momento, si se agregara mayor información
        #y más precisa, este filtro podría ser tenido en cuenta para más precisión
        #if distancias[i] > 8:
        #    continue

        fuente = metadatas[i]["source"]

        if fuente not in fuentes_usadas:

            contexto += (
                f"\n[Fuente {contador} - {fuente}]\n"
                f"{documentos[i]}\n"
            )

            evidencia += (
                f"[{contador}] "
                f"Fuente: {fuente} | "
                f"Distancia semántica: {distancias[i]:.4f}\n"
            )

            fuentes.append(fuente)

            fuentes_usadas.add(fuente)

            contador += 1

        if contador > 3:
            break

    return contexto, evidencia, list(set(fuentes))