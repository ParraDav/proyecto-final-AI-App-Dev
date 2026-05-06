import ollama
import re
from rag_engine import buscar_contexto

def analista_soporte_chat():

    print("========================================================")
    print("      ANALISTA INTELIGENTE DE SOPORTE TÉCNICO CON RAG")
    print("========================================================")
    print("Sistema inicializado correctamente.")
    print("Escribe tu problema técnico.")
    print("Escribe 'salir' para terminar.\n")

    while True:

        problema_usuario = input("Usuario: ")

        if problema_usuario.lower() == "salir":
            print("Asistente: Conversación finalizada.")
            break

        print("\nBuscando contexto técnico en base vectorial...\n")

        contexto_rag, evidencia = buscar_contexto(problema_usuario)

        print("=========== EVIDENCIA DE RECUPERACIÓN RAG ===========")
        print(evidencia)
        print("=====================================================\n")

        print("Generando diagnóstico técnico con Gemma3...\n")

        prompt = f"""
Eres un Analista Inteligente de Soporte Técnico especializado en:

- computadoras
- hardware
- software
- redes e internet
- impresoras y periféricos

Tu función es diagnosticar el problema técnico del usuario utilizando PRIORITARIAMENTE
la siguiente base de conocimientos recuperada por el sistema RAG.

Debes fundamentar tu respuesta en la evidencia documental suministrada.
No debes inventar información ajena al contexto técnico.

=========== BASE DE CONOCIMIENTOS RECUPERADA ===========
{contexto_rag}
========================================================

INSTRUCCIONES:
1. Detecta el problema técnico principal.
2. Explica la causa más probable.
3. Propón una solución paso a paso.
4. Genera siempre una recomendación adicional útil.
5. Si la consulta no pertenece al dominio tecnológico, indícalo.
6. Responde EXCLUSIVAMENTE en JSON válido.

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

        match = re.search(r'\{.*\}', respuesta_modelo, re.DOTALL)

        print("Asistente:")
        if match:
            print(match.group())
        else:
            print(respuesta_modelo)

        print()

analista_soporte_chat()