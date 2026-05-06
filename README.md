# Proyecto Final - Analista Inteligente de Soporte Técnico con IA y Sistema RAG

---

## Descripción del proyecto

Este proyecto implementa un asistente conversacional inteligente que actúa como un **Analista de Soporte Técnico Automatizado**, capaz de diagnosticar problemas básicos relacionados con:

- computadores
- sistema operativo Windows
- redes e internet
- impresoras y periféricos
- hardware básico
- mantenimiento de software

El sistema permite que el usuario describa en lenguaje natural un inconveniente tecnológico y reciba un análisis estructurado con:

- problema detectado,
- posible causa,
- solución paso a paso,
- recomendación adicional.

A diferencia de un chatbot tradicional, esta segunda versión incorpora un **sistema RAG (Retrieval Augmented Generation)**, lo que significa que antes de generar una respuesta, el asistente consulta una **base documental vectorizada** de conocimientos técnicos y utiliza esa información como contexto para producir diagnósticos más precisos y fundamentados.

La interacción se realiza mediante un **chat en consola**.

---

## Objetivo del asistente

Desarrollar un sistema inteligente capaz de:

- Analizar consultas técnicas realizadas por el usuario.
- Recuperar automáticamente información relevante desde una base de conocimientos.
- Utilizar dicha información para enriquecer el prompt del modelo de lenguaje.
- Generar respuestas estructuradas en formato JSON.
- Simular el comportamiento de un analista de soporte técnico básico.

---

## Tecnologías utilizadas

Este proyecto fue desarrollado con las siguientes tecnologías:

- **Python**
- **Ollama**
- **Gemma3** (modelo generador)
- **nomic-embed-text** (modelo de embeddings)
- **ChromaDB** (base de datos vectorial)
- **Prompt Engineering**
- **Sistema RAG (Retrieval Augmented Generation)**

---

## Arquitectura general del sistema

El proyecto está compuesto por tres módulos principales:

### 1. Módulo de ingestión documental (`ingest_documents.py`)

Este módulo se encarga de:

- leer todos los documentos de la carpeta `knowledge_base`,
- extraer texto desde archivos `.txt` y `.pdf`,
- dividir el contenido en chunks semánticos,
- generar embeddings vectoriales usando `nomic-embed-text`,
- almacenar dichos embeddings en ChromaDB.

---

### 2. Módulo de recuperación RAG (`rag_engine.py`)

Este archivo implementa el mecanismo de recuperación de contexto:

- recibe la consulta del usuario,
- genera el embedding de la pregunta,
- consulta la base vectorial,
- recupera los chunks más cercanos semánticamente,
- construye el contexto técnico que será enviado al LLM.

Además, el sistema muestra en consola la **evidencia documental recuperada**, permitiendo visualizar el funcionamiento del retrieval.

---

### 3. Módulo conversacional principal (`proyecto.py`)

Este es el chat principal del sistema.

Su función es:

- recibir el problema del usuario,
- solicitar contexto al motor RAG,
- construir un prompt aumentado con la evidencia técnica recuperada,
- enviar el prompt al modelo Gemma3,
- recibir la respuesta del modelo,
- limpiar y mostrar el JSON final.

---

## Flujo completo del sistema RAG implementado

El pipeline implementado funciona de la siguiente manera:

Usuario realiza consulta
↓
Se genera embedding de la pregunta
↓
Consulta semántica en ChromaDB
↓
Recuperación de chunks documentales relevantes
↓
Construcción de contexto técnico
↓
Prompt aumentado (Prompt Engineering + Contexto RAG)
↓
Gemma3 genera diagnóstico técnico
↓
Salida estructurada en JSON

Este flujo permite que el modelo no dependa únicamente de su conocimiento interno, sino que utilice información documental específica previamente cargada.

---

## Base de conocimientos utilizada (`knowledge_base`)

Para construir el sistema RAG se diseñó una base de conocimientos híbrida compuesta por:

### Documentos curados manualmente (.txt)

- `hardware_basico.txt`
- `impresoras_perifericos.txt`
- `redes_wifi.txt`
- `software_mantenimiento.txt`
- `windows_problemas.txt`

Estos archivos contienen casos comunes de soporte técnico con:

- síntomas,
- posibles causas,
- procedimientos de solución.

---

### Documentación técnica externa (.pdf)

- `hp_network_troubleshooting.pdf`
- `ms_printer_troubleshooting.pdf`
- `ms_stopcode.pdf`

Estos documentos fueron obtenidos desde documentación oficial de soporte técnico de HP y Microsoft para aportar información real de troubleshooting.

---

## Chunking y vectorización documental

Cada documento fue fragmentado en pequeños bloques de texto llamados **chunks**, con el fin de mejorar la recuperación semántica.

Se utilizó una estrategia de:

- `chunk_size` aproximado de 120 palabras
- `overlap` de 30 palabras

Esto permite conservar continuidad contextual entre fragmentos consecutivos.

Posteriormente, cada chunk fue convertido en embedding vectorial usando:

- modelo `nomic-embed-text`

Finalmente todos los embeddings fueron almacenados en una colección de ChromaDB llamada:

`soporte_tecnico`

La base vectorial final quedó conformada por **64 chunks documentales**.

---

## Técnicas de Prompt Engineering utilizadas

Además del RAG, el proyecto mantiene varias estrategias de Prompt Engineering:

### 1. Role Prompting / System Configuration

El modelo es configurado como:

> Analista Inteligente de Soporte Técnico

especializado en:

- hardware
- software
- redes
- impresoras
- mantenimiento de computadores

---

### 2. Context Injection

El contexto recuperado desde ChromaDB es insertado dentro del prompt antes de la consulta del usuario.

Esto convierte al prompt en un **Prompt Aumentado por Recuperación**.

---

### 3. Output Constraining

Se obliga al modelo a responder exclusivamente en formato JSON para garantizar uniformidad estructural.

---

## Formato de salida del asistente

El sistema genera respuestas con el siguiente formato:

```json
{
 "problema_detectado": "",
 "posible_causa": "",
 "solucion_paso_a_paso": [],
 "recomendacion_adicional": ""
}
```

---

## Ejemplo de funcionamiento

### Consulta del usuario

mi impresora no imprime

### Evidencia de recuperación RAG

Resultado 1 | Fuente documental recuperada: impresoras_perifericos.txt  
Resultado 2 | Fuente documental recuperada: ms_printer_troubleshooting.pdf  
Resultado 3 | Fuente documental recuperada: hardware_basico.txt

### Respuesta generada

```json
{
 "problema_detectado": "La impresora no imprime",
 "posible_causa": "Las causas más comunes son estado offline, cola de impresión detenida o controlador dañado.",
 "solucion_paso_a_paso": [
  "Verificar que la impresora esté encendida",
  "Revisar la conexión USB o WiFi",
  "Cancelar trabajos pendientes en la cola de impresión",
  "Reiniciar el servicio spooler",
  "Reinstalar drivers de la impresora"
 ],
 "recomendacion_adicional": "Configurar la impresora como dispositivo predeterminado"
}
```

---

## Requisitos de instalación

- Python 3.10 o superior
- Ollama instalado

Modelos necesarios:

```bash
ollama pull gemma3
ollama pull nomic-embed-text
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Ejecución del proyecto

### 1. Construir base vectorial

```bash
python ingest_documents.py
```

### 2. Ejecutar asistente conversacional

```bash
python proyecto.py
```

---

## Estructura del repositorio

```bash
proyecto-final-AI-App-Dev/
│
├── knowledge_base/
│   ├── hardware_basico.txt
│   ├── impresoras_perifericos.txt
│   ├── redes_wifi.txt
│   ├── software_mantenimiento.txt
│   ├── windows_problemas.txt
│   ├── hp_network_troubleshooting.pdf
│   ├── ms_printer_troubleshooting.pdf
│   └── ms_stopcode.pdf
│
├── chroma_db/
├── ingest_documents.py
├── rag_engine.py
├── proyecto.py
├── requirements.txt
└── README.md
```

---

## Conclusión

La incorporación del sistema RAG permitió transformar un chatbot basado únicamente en prompting en un asistente con capacidad de:

- consultar una base de conocimientos propia,
- fundamentar técnicamente sus respuestas,
- mostrar evidencia documental recuperada,
- y generar diagnósticos más consistentes.

Este proyecto demuestra la integración funcional entre:

- Prompt Engineering,
- Embeddings,
- Base de Datos Vectorial,
- Recuperación Semántica,
- y Generación con LLM.