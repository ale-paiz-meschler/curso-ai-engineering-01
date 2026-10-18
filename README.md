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