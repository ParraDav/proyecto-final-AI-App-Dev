import ollama

ollama.pull("gemma3")

def analista_soporte_chat():

    system_prompt = """
Eres un Analista de Soporte Técnico especializado en diagnosticar
problemas básicos de computadoras, software e internet.

Reglas:
1. Analiza el problema del usuario.
2. Identifica el problema técnico.
3. Explica la posible causa.
4. Proporciona una solución paso a paso.
5. Responde en formato JSON.
6. Si la pregunta del usuario no está relacionada con soporte técnico
(computadoras, software, redes, hardware o dispositivos), debes
responder indicando que la consulta está fuera del alcance del asistente.


Formato obligatorio:

{
 "problema_detectado": "",
 "posible_causa": "",
 "solucion_paso_a_paso": [],
 "recomendacion_adicional": ""
}
"""

    ejemplos = """
EJEMPLO 1 (CASO DE SOPORTE TÉCNICO)

Problema:
El computador está muy lento al iniciar.

Respuesta:

{
 "problema_detectado": "Inicio lento del sistema",
 "posible_causa": "Demasiados programas ejecutándose al iniciar",
 "solucion_paso_a_paso": [
  "Abrir el administrador de tareas",
  "Ir a la pestaña Inicio",
  "Desactivar programas innecesarios"
 ],
 "recomendacion_adicional": "Revisar el estado del disco duro"
}

EJEMPLO 2 (CASO FUERA DEL DOMINIO)

Problema:
¿Cómo hago galletas en casa sin horno?

Respuesta:

{
 "problema_detectado": "Consulta fuera del dominio de soporte técnico",
 "posible_causa": "La pregunta está relacionada con cocina y no con problemas tecnológicos",
 "solucion_paso_a_paso": [],
 "recomendacion_adicional": "Realiza una consulta relacionada con computadoras, software, redes o dispositivos."
}
"""

    print("Asistente de Soporte Técnico")
    print("Escribe tu problema técnico.")
    print("Escribe 'salir' para terminar.\n")

    while True:

        problema_usuario = input("Usuario: ")

        if problema_usuario.lower() == "salir":
            print("Asistente: Conversación finalizada.")
            break

        prompt = f"""
{system_prompt}

{ejemplos}

<<<PROBLEMA_DEL_USUARIO>>>
{problema_usuario}
<<<FIN_PROBLEMA>>>
"""

        response = ollama.chat(
            model="gemma3",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        print("\nAsistente:")
        print(response["message"]["content"])
        print()


analista_soporte_chat()
