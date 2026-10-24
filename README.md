# Pre-entrega 1: Cliente de LLM robusto y asíncrono

Este proyecto fue desarrollado utilizando **Visual Studio Code** en una notebook con **Ubuntu 24.04.2 LTS**. 

> **Nota de entorno:** Debido a las restricciones de una máquina corporativa sin permisos de administrador (`sudo`), el flujo de instalación tradicional del sistema operativo fue adaptado utilizando **`uv`**, permitiendo configurar un entorno aislado sin requerir privilegios elevados.


## 🛠️ Configuración del Entorno (Sin permisos de Administrador)

Para sortear las limitaciones de instalación de paquetes del sistema (`apt` / `ensurepip`), se utilizó **`uv`**, una herramienta moderna escrita en Rust desarrollada por Astral. Este binario autónomo permite gestionar entornos virtuales y dependencias de forma ultrarrápida en el espacio de usuario.

Ejecutar los siguientes comandos en la terminal para replicar el entorno:

1. **Instalación local de `uv` y creación del entorno virtual con Python 3.12:**
   ```bash
   curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
   source $HOME/.local/bin/env
   uv --version
   uv venv --python 3.12

2. **Activación del entorno virtual:**
   ```bash
   source .venv/bin/activate

3. **Instalación de dependencias requeridas:**
   ```bash
   uv pip install openai anthropic pydantic python-dotenv google-genai

4. **Archivo de prueba para asegurarme de que todo se importa correctamente**
   ```bash
   echo 'import openai; import anthropic; import pydantic; import dotenv; print("¡Todo funciona a la perfección!")' > test.py
   python3 test.py

5. **Comando para ejecutar esta entrega**
   ```bash
   python3 main.py

## ⚙️ Configuración de Credenciales (`.env`)

Por motivos de seguridad, las claves de API **no** se encuentran hardcodeadas en el código fuente para evitar bloqueos al subir el repositorio a GitHub. 

Se creó un archivo llamado `.env` en la raíz del proyecto, que fue agregado al .gitignore y está basado en este formato:

```env
OPENAI_API_KEY=clave_real_de_openai
ANTHROPIC_API_KEY=clave_real_de_anthropic
GOOGLE_API_KEY=clave_real_de_google
```

# Ejercicio opcional sobre Unidad 1: Embeddings y similitud

## Para esta entrega hay que observar el siguiente archivo:
similitud.py: Script complementario de recuperación léxica mediante TF-IDF y Similitud Coseno sobre un corpus técnico diversificado.


# Pre-entrega 2: Pipeline de procesamiento validado

## Para esta entrega, se deben observar los siguientes archivos:

1. **schemas.py: Modelos de datos estructurados utilizando Pydantic, con validadores estrictos y enumeraciones (NivelCriticidad) para asegurar esquemas de salida tipados.**

2. **pipeline.py / chain.py: Implementación de la cadena LCEL (prompt | model.with_structured_output(Schema)) combinada con políticas de resiliencia y reintentos automáticos (.with_retry()). Incluye la función asíncrona process_text(text: str) mediante .ainvoke().**

3. **main_pipeline.py: Script de ejecución que evalúa casos de prueba reales y pruebas de estrés con textos ambiguos.**

# Pre-entrega 3: Sistema de recuperación semántica local (RAG)

1. **ingest.py: Módulo encargado de leer archivos Markdown locales de la carpeta /data, aplicar un chunking estratégico (RecursiveCharacterTextSplitter, tamaño 500 con overlap de 50), y persistir los embeddings en una instancia local de ChromaDB en ./vectorstore (incluyendo control de persistencia para evitar reindexaciones innecesarias).** 

2. **rag_chain.py: Define la función asíncrona get_rag_response(query: str), configurando un retriever optimizado (top_k=3 para evitar contexto infinito), un prompt de sistema con estricto filtro de veracidad ("No lo sé"), y un modelo de salida estructurado en Pydantic que incluye respuesta, referencias de archivos y validación de contexto.**

3. **main_rag.py: Script de ejecución principal que valida el flujo completo. Le pide al usuario que ingrese una consulta y la valida sobre los documentos locales.**

4. **Se configuró el chunking basado en tokens reales utilizando RecursiveCharacterTextSplitter.from_tiktoken_encoder (mínimo de 500 tokens), se incorporó un archivo requirements.txt para garantizar la reproducibilidad del entorno, y se configuró un registro automático de pruebas obligatorias (válida y trampa) en la ejecución inicial de main_rag.py para demostrar la robustez antialucinación del sistema RAG.**

# Pre-entrega 4: Sistema RAG escalable en la nube con Pinecone

## Para esta entrega, se deben observar los siguientes archivos:

1. **/data/dberrors.csv: Incorporación de un set de datos tabular estructurado con 250 registros de códigos de error de los 5 principales motores de bases de datos relacionales (Microsoft SQL Server, Oracle, DB2, PostgreSQL y MySQL), diseñado específicamente para potenciar la precisión de la recuperación léxica.**
2. **ingest_pinecone.py: Pipeline de Ingesta en la Nube. Procesa los registros aplicando un chunking estratégico basado en tokens (con el tokenizador de OpenAI y un tamaño de 600 tokens con overlap de 60). Se conecta a Pinecone Serverless utilizando vectores densos de 1536 dimensiones (text-embedding-3-small) y organizando la información mediante un namespace dedicado (db-errors). Almacena el texto original y metadatos avanzados directamente en el índice, evitando llamadas a bases de datos relacionales externas.**
3. **hybrid_retriever.py: Recuperador Híbrido. Implementa un EnsembleRetriever que combina de forma ponderada la búsqueda semántica densa de Pinecone (60%) con la búsqueda léxica exacta de BM25 (40%). Esto garantiza una precisión quirúrgica tanto para conceptos abstractos como para códigos de error alfanuméricos exactos (ej. 2627, ORA-00942).**
4. **evaluate_rag.py y golden_set.json: Script de Evaluación con Golden Set. Utiliza un conjunto de preguntas de prueba técnicas de alta precisión para medir de forma automatizada las métricas fundamentales del sistema (Precision@5 y Recall@5), validando el rendimiento de la recuperación.**

Instrucciones de ejecución para esta entrega

1. **Instalación local de `uv` y creación del entorno virtual con Python 3.12:**
   ```bash
   curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
   source $HOME/.local/bin/env
   uv --version
   uv venv --python 3.12

2. **Subir y poblar la base vectorial en la nube::**
   ```bash
   python3 ingest_pinecone.py

3. **Probar el recuperador híbrido de manera aislada**
   ```bash
   python3 hybrid_retriever.py

4. **Ejecutar la evaluación formal de rendimiento**
   ```bash
   python3 evaluate_rag.py