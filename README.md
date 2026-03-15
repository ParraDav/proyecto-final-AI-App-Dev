# Proyecto Final - Asistente de Soporte Técnico con IA

## Descripción

Este proyecto implementa un asistente conversacional que actúa como **analista de soporte técnico**.  
El sistema permite a un usuario describir un problema tecnológico (por ejemplo, problemas de conexión, rendimiento del computador o dispositivos periféricos) y recibir un diagnóstico junto con posibles soluciones.

El asistente utiliza **técnicas de Prompt Engineering** para controlar el comportamiento del modelo de lenguaje y generar respuestas estructuradas y consistentes en formato JSON.

El sistema funciona mediante interacción tipo **chat en consola**, donde el usuario puede escribir su problema y recibir una respuesta automática del asistente.

---

# Objetivo del asistente

El objetivo del proyecto es desarrollar un asistente capaz de:

- Analizar problemas técnicos descritos por el usuario.
- Identificar posibles causas del problema.
- Proporcionar soluciones paso a paso.
- Mantener una interacción tipo chat mediante la consola.
- Generar respuestas estructuradas que puedan ser interpretadas por otros sistemas.

---

# Tecnologías utilizadas

Este proyecto utiliza las siguientes tecnologías:

- **Python**
- **Ollama**
- **Modelo de lenguaje:** Gemma 3
- **Prompt Engineering**

---

# Técnicas de Prompt Engineering utilizadas

## 1. System Prompt

El **System Prompt** define el rol del modelo y las reglas que debe seguir durante la conversación.

En este proyecto, el modelo es configurado como un **Analista de Soporte Técnico**, especializado en diagnosticar problemas relacionados con:

- computadoras
- software
- redes
- hardware
- dispositivos tecnológicos

Además, el System Prompt establece que la respuesta debe generarse **siempre en formato JSON**.

---

## 2. Few-Shot Prompting

Se incluyen ejemplos de problemas técnicos junto con sus respuestas esperadas para guiar el comportamiento del modelo.

Estos ejemplos permiten que el modelo aprenda:

- la estructura de respuesta
- el tipo de diagnóstico esperado
- el formato JSON requerido

También se incluye un ejemplo de **consulta fuera del dominio** para que el asistente identifique cuando una pregunta no está relacionada con soporte técnico.

---

## 3. Uso de delimitadores

Se utilizan delimitadores para separar claramente el problema del usuario del resto de instrucciones del prompt.

Ejemplo:

<<<PROBLEMA_DEL_USUARIO>>>
No puedo conectarme al WiFi
<<<FIN_PROBLEMA>>>


Esto evita que el modelo confunda la consulta del usuario con las instrucciones del sistema.

---

# Formato de salida

El asistente genera respuestas estructuradas en formato JSON con el siguiente formato:

{
"problema_detectado": "",
"posible_causa": "",
"solucion_paso_a_paso": [],
"recomendacion_adicional": ""
}


Ejemplo de respuesta:

{
"problema_detectado": "Conexión WiFi no disponible",
"posible_causa": "Adaptador de red desactivado",
"solucion_paso_a_paso": [
"Verificar si el WiFi está activado",
"Reiniciar el router",
"Actualizar los controladores de red"
],
"recomendacion_adicional": "Intentar conectarse a otra red"
}


---

# Requisitos

Para ejecutar el proyecto se necesita:

- **Python 3.10 o superior**
- **Ollama instalado en el sistema**

Instalar Ollama desde:

https://ollama.com/

El modelo utilizado en este proyecto es **gemma3**.

---

# Instalación

Instalar las dependencias del proyecto a traves de la terminal:

pip install -r requirements.txt


El programa descargará automáticamente el modelo necesario si no está disponible en el sistema.

También puede descargarse manualmente con:

ollama pull gemma3


---

# Ejecución del programa

Para ejecutar el asistente, escribir en la terminal:

python proyecto.py

El sistema iniciará un chat en consola donde el usuario podrá describir su problema técnico.