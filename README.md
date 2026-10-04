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