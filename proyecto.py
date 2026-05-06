import ollama
from rag_engine import buscar_contexto

def analista_soporte_chat():

    print("==========================================")
    print("   ANALISTA DE SOPORTE TÉCNICO CON RAG")
    print("==========================================")
    print("Escribe tu problema técnico.")
    print("Escribe 'salir' para terminar.\n")

    while True:

        problema_usuario = input("Usuario: ")

        if problema_usuario.lower() == "salir":
            print("Asistente: Conversación finalizada.")
            break

        # =========================
        # RECUPERACIÓN RAG
        # =========================
        contexto_rag = buscar_contexto(problema_usuario)

        print("\n--- CHUNKS RECUPERADOS POR EL RAG ---")
        print(contexto_rag)
        print("-------------------------------------\n")

        # =========================
        # PROMPT AUMENTADO
        # =========================
        prompt = f"""
Eres un Analista de Soporte Técnico especializado en diagnosticar
problemas básicos de computadoras, software, internet y dispositivos.

Debes responder basándote PRIORITARIAMENTE en la siguiente base de conocimientos recuperada:

{contexto_rag}

Reglas:
1. Analiza el problema del usuario.
2. Identifica el problema técnico.
3. Explica la posible causa.
4. Proporciona una solución paso a paso.
5. Responde únicamente en formato JSON.
6. Si la pregunta no corresponde a soporte técnico, indícalo.

Formato obligatorio:

{{
 "problema_detectado": "",
 "posible_causa": "",
 "solucion_paso_a_paso": [],
 "recomendacion_adicional": ""
}}

<<<PROBLEMA_DEL_USUARIO>>>
{problema_usuario}
<<<FIN_PROBLEMA>>>
"""

        response = ollama.chat(
            model="gemma3",
            messages=[{"role": "user", "content": prompt}]
        )

        print("Asistente:")
        print(response["message"]["content"])
        print()

analista_soporte_chat()