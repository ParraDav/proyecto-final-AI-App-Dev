import os
import ollama
import chromadb
from pypdf import PdfReader

# =====================================================
# CONFIGURACIÓN CHROMADB
# =====================================================

client = chromadb.PersistentClient(path="./chroma_db")

# Eliminar colección anterior para evitar duplicados
try:
    client.delete_collection("soporte_tecnico")
except:
    pass

collection = client.get_or_create_collection(
    name="soporte_tecnico"
)

# =====================================================
# LEER TXT
# =====================================================

def leer_txt(ruta):

    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()

# =====================================================
# LEER PDF
# =====================================================

def leer_pdf(ruta):

    texto = ""

    reader = PdfReader(ruta)

    for page in reader.pages:

        contenido = page.extract_text()

        if contenido:
            texto += contenido + "\n"

    return texto

# =====================================================
# CHUNKING
# =====================================================

def dividir_texto(texto, chunk_size=450, overlap=80):

    palabras = texto.split()

    chunks = []

    inicio = 0

    while inicio < len(palabras):

        fin = inicio + chunk_size

        chunk = " ".join(
            palabras[inicio:fin]
        )

        chunks.append(chunk)

        inicio += chunk_size - overlap

    return chunks

# =====================================================
# CARGA DOCUMENTOS
# =====================================================

carpeta = "knowledge_base"

contador = 0

for archivo in os.listdir(carpeta):

    ruta = os.path.join(carpeta, archivo)

    # ==========================================
    # TXT
    # ==========================================

    if archivo.endswith(".txt"):

        texto = leer_txt(ruta)

    # ==========================================
    # PDF
    # ==========================================

    elif archivo.endswith(".pdf"):

        texto = leer_pdf(ruta)

    else:
        continue

    # ==========================================
    # CHUNKING
    # ==========================================

    chunks = dividir_texto(texto)

    print(f"\nProcesando: {archivo}")
    print(f"Chunks generados: {len(chunks)}")

    # ==========================================
    # EMBEDDINGS
    # ==========================================

    for i, chunk in enumerate(chunks):

        embedding = ollama.embeddings(
            model="nomic-embed-text",
            prompt=chunk
        )["embedding"]

        collection.add(
            ids=[f"{archivo}_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{
                "source": archivo,
                "chunk": i
            }]
        )

        contador += 1

print("\n========================================")
print(f"Base vectorial creada correctamente.")
print(f"Total chunks almacenados: {contador}")
print("========================================")