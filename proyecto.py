import ollama
import re
from rag_engine import buscar_contexto

def analista_soporte_chat():

    print("==============================================")
    print("   ANALISTA DE SOPORTE TÉCNICO CON SISTEMA RAG")
    print("==============================================")
    print("Escribe tu problema técnico.")
    print("Escribe 'salir' para terminar.\n")

    while True:

        problema_usuario = input("Usuario: ")

        if problema_usuario.lower() == "salir":
            print("Asistente: Conversación finalizada.")
            break

        # ======================================
        # RECUPERAR CONTEXTO DESDE RAG
        # ======================================
        contexto_rag, evidencia = buscar_contexto(problema_usuario)

        print("\n=========== EVIDENCIA DE RECUPERACIÓN RAG ===========")
        print(evidencia)
        print("=====================================================\n")

        # ======================================
        # PROMPT ENGINEERING + CONTEXTO RAG
        # ======================================
        prompt = f"""
Eres un Analista Inteligente de Soporte Técnico especializado en:

- computadoras
- hardware
- software
- redes e internet
- impresoras y periféricos

Tu función es diagnosticar el problema técnico del usuario utilizando PRIORITARIAMENTE
la siguiente base de conocimientos recuperada por el sistema RAG.

No debes inventar información que no esté relacionada con el contexto técnico.
Debes analizar la consulta y generar una respuesta estructurada.

=========== BASE DE CONOCIMIENTOS RECUPERADA ===========
{contexto_rag}
========================================================

INSTRUCCIONES:
1. Detecta el problema técnico principal.
2. Explica la causa más probable.
3. Propón una solución paso a paso.
4. Si la consulta no pertenece al dominio tecnológico, indícalo.
5. Responde EXCLUSIVAMENTE en JSON válido.

Formato obligatorio:

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
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        respuesta_modelo = response["message"]["content"]

        # ======================================
        # LIMPIEZA DEL JSON
        # ======================================
        match = re.search(r'\{.*\}', respuesta_modelo, re.DOTALL)

        print("Asistente:")
        if match:
            print(match.group())
        else:
            print(respuesta_modelo)

        print()

analista_soporte_chat()