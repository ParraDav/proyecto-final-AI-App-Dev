import streamlit as st
import json

from app import generar_respuesta

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Analista Inteligente de Soporte Técnico",
    layout="wide"
)

# =====================================================
# TÍTULO
# =====================================================

st.title("Analista Inteligente de Soporte Técnico con RAG")

st.markdown("""
Sistema de soporte técnico especializado utilizando:

- Ollama
- ChromaDB
- Embeddings semánticos
- Retrieval-Augmented Generation (RAG)
""")

# =====================================================
# INPUT USUARIO
# =====================================================

pregunta = st.text_input(
    "Describe tu problema técnico"
)

# =====================================================
# BOTÓN CONSULTAR
# =====================================================

if st.button("Consultar"):

    if pregunta.strip() == "":

        st.warning("Por favor escribe una consulta.")

    else:

        with st.spinner("Analizando problema técnico..."):

            respuesta, evidencia, fuentes = generar_respuesta(
                pregunta
            )

        # ==========================================
        # RESPUESTA
        # ==========================================

        st.subheader("Diagnóstico generado")

        try:

            respuesta_json = json.loads(respuesta)

            st.json(respuesta_json)

        except:

            st.text(respuesta)

        # ==========================================
        # FUENTES
        # ==========================================

        st.subheader("Fuentes documentales")

        for fuente in fuentes:
            st.write(f"• {fuente}")

        # ==========================================
        # EVIDENCIA RAG
        # ==========================================

        st.subheader("Evidencia de recuperación semántica")

        st.text(evidencia)