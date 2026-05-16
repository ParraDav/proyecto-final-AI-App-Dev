import ollama
import json
from rag_engine import buscar_contexto


# =====================================================
# FUNCIÓN PRINCIPAL DE GENERACIÓN
# =====================================================

def generar_respuesta(problema_usuario):

    contexto_rag, evidencia, fuentes = buscar_contexto(problema_usuario)

    # ==========================================
    # VALIDACIÓN DE CONTEXTO VACÍO
    # ==========================================

    if not contexto_rag.strip():

        respuesta_error = {
            "problema_detectado": "Sin información",
            "posible_causa": "No existe información suficiente en la base de conocimiento",
            "solucion_paso_a_paso": [
                "No encuentro esa información en la base de conocimiento."
            ],
            "recomendacion_adicional": "Realiza una consulta relacionada con soporte técnico."
        }

        return json.dumps(
    respuesta_error,
    ensure_ascii=False,
    indent=4
), evidencia, fuentes

    # ==========================================
    # PROMPT RAG
    # ==========================================

    prompt = f"""
Eres un Analista Inteligente de Soporte Técnico especializado en:

- computadoras
- hardware
- software
- redes e internet
- impresoras y periféricos

Tu función es diagnosticar problemas técnicos utilizando EXCLUSIVAMENTE
la información presente en el contexto recuperado por el sistema RAG.

========================================================
BASE DE CONOCIMIENTOS RECUPERADA
========================================================

{contexto_rag}

========================================================

REGLAS IMPORTANTES:

1. Responde ÚNICAMENTE usando el contexto recuperado.
2. Si la información no aparece en el contexto, responde exactamente:
   "No encuentro esa información en la base de conocimiento."
3. No inventes soluciones.
4. No supongas configuraciones técnicas.
5. No generes pasos inexistentes.
6. Si la consulta no pertenece al dominio tecnológico, indícalo.
7. Responde EXCLUSIVAMENTE en JSON válido.

FORMATO OBLIGATORIO:

{{
    "problema_detectado": "",
    "posible_causa": "",
    "solucion_paso_a_paso": [],
    "recomendacion_adicional": ""
}}

CONSULTA DEL USUARIO:
{problema_usuario}
"""

    response = ollama.chat(
        model="gemma3",
        format="json",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    respuesta_modelo = response["message"]["content"]

    return respuesta_modelo, evidencia, fuentes


# =====================================================
# CHAT POR CONSOLA
# =====================================================

def analista_soporte_chat():

    print("========================================================")
    print("      ANALISTA INTELIGENTE DE SOPORTE TÉCNICO")
    print("========================================================")
    print("Sistema inicializado correctamente.")
    print("Escribe tu problema técnico.")
    print("Escribe 'salir' para terminar.\n")

    while True:

        problema_usuario = input("Usuario: ")

        if problema_usuario.lower() == "salir":
            print("Asistente: Conversación finalizada.")
            break

        print("\nBuscando información técnica...\n")

        respuesta, evidencia, fuentes = generar_respuesta(problema_usuario)

        print("=========== EVIDENCIA RAG ===========")
        print(evidencia)

        print("\n=========== FUENTES ===========")

        for fuente in fuentes:
            print(f"- {fuente}")

        print("\n=========== RESPUESTA ===========")
        print(respuesta)
        print()


# =====================================================
# EJECUCIÓN
# =====================================================

if __name__ == "__main__":
    analista_soporte_chat()