import os
import ollama
import chromadb
from pypdf import PdfReader

# =========================
# CONFIGURACIÓN CHROMA
# =========================
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="soporte_tecnico")

# =========================
# FUNCIÓN LEER TXT
# =========================
def leer_txt(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()

# =========================
# FUNCIÓN LEER PDF
# =========================
def leer_pdf(ruta):
    texto = ""
    reader = PdfReader(ruta)
    for page in reader.pages:
        contenido = page.extract_text()
        if contenido:
            texto += contenido + "\n"
    return texto

# =========================
# CHUNKING
# =========================
def dividir_texto(texto, chunk_size=220, overlap=40):
    palabras = texto.split()
    chunks = []

    inicio = 0
    while inicio < len(palabras):
        fin = inicio + chunk_size
        chunk = " ".join(palabras[inicio:fin])
        chunks.append(chunk)
        inicio += chunk_size - overlap

    return chunks

# =========================6
# CARGAR TODOS LOS DOCUMENTOS
# =========================
carpeta = "knowledge_base"
contador = 0

for archivo in os.listdir(carpeta):

    ruta = os.path.join(carpeta, archivo)

    if archivo.endswith(".txt"):
        texto = leer_txt(ruta)

    elif archivo.endswith(".pdf"):
        texto = leer_pdf(ruta)

    else:
        continue

    chunks = dividir_texto(texto)

    print(f"\nProcesando {archivo} | chunks generados: {len(chunks)}")

    for i, chunk in enumerate(chunks):

        embedding = ollama.embeddings(
            model="nomic-embed-text",
            prompt=chunk
        )["embedding"]

        collection.add(
            ids=[f"{archivo}_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"source": archivo}]
        )

        contador += 1

print(f"\nBase vectorial creada correctamente con {contador} chunks.")