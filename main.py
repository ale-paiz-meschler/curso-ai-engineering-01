import asyncio
import os
from getpass import getpass
from dotenv import load_dotenv

# Bloque de validación y respaldo de API Keys (sin exponer secretos en el código)
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass("🔑 OPENAI_API_KEY: ").strip()

if not os.environ.get("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = getpass("🔑 ANTHROPIC_API_KEY: ").strip()

if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass("🔑 GOOGLE_API_KEY: ").strip()

from pydantic import SecretStr
from schemas import LLMConfig, Provider, ChatMessage
from clients import AsyncLLMManager

async def main():
    print("\n🚀 Ejecutando pruebas de la entrega...\n")
    
    pregunta = [ChatMessage(role="user", content="¿Qué es la entropía? Respondé en 2 líneas.")]

    # --- 1. Prueba en modo normal (OpenAI) ---
    config_openai = LLMConfig(
        provider=Provider.OPENAI,
        model="gpt-4o-mini",
        openai_api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
        temperature=0.7,
        max_tokens=200,
    )
    manager_openai = AsyncLLMManager(config_openai)
    resultado_openai = await manager_openai.generate(pregunta)
    print("🟢 OpenAI:", resultado_openai.content if not resultado_openai.error else f"❌ {resultado_openai.error}")

    # --- 2. Prueba en modo normal (Anthropic) ---
    config_anthropic = LLMConfig(
        provider=Provider.ANTHROPIC,
        model="claude-3-5-sonnet-latest",  # Modelo actual y válido de Anthropic
        anthropic_api_key=SecretStr(os.environ["ANTHROPIC_API_KEY"]),
        temperature=0.7,
        max_tokens=200,
    )
    manager_anthropic = AsyncLLMManager(config_anthropic)
    resultado_anthropic = await manager_anthropic.generate(pregunta)
    print("🟣 Anthropic:", resultado_anthropic.content if not resultado_anthropic.error else f"❌ {resultado_anthropic.error}")

    # --- 3. Prueba en modo streaming (OpenAI) ---
    print("\n🟢 Streaming OpenAI:")
    async for chunk in manager_openai.generate_stream(pregunta):
        print(chunk, end="", flush=True)

    # --- 4. Prueba en modo streaming (Anthropic) ---
    print("\n\n🟣 Streaming Anthropic:")
    async for chunk in manager_anthropic.generate_stream(pregunta):
        print(chunk, end="", flush=True)
    print("\n")

    # --- 5. Prueba de resiliencia (Manejo de errores / API key inválida) ---
    config_rota = LLMConfig(
        provider=Provider.OPENAI,
        model="gpt-4o-mini",
        openai_api_key=SecretStr("sk-key-invalida-a-proposito"),
    )
    manager_roto = AsyncLLMManager(config_rota)
    resultado_roto = await manager_roto.generate(pregunta)

    print("¿El programa siguió vivo tras el error?: ✅ Sí")
    print("Error controlado capturado:", resultado_roto.error)

if __name__ == "__main__":
    asyncio.run(main())