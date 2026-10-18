import asyncio
from ingest import inicializar_base_vectorial
from rag_chain import get_rag_response

async def main():
    print("🚀 Inicializando el Sistema RAG End-to-End...")

    inicializar_base_vectorial()

    print("\n" + "="*60)
    print("🤖 ¡Sistema RAG listo para recibir consultas!")
    print("   - Escribe tu pregunta y presiona Enter.")
    print("   - Escribe 'salir' o 'exit' para terminar la ejecución.")
    print("="*60 + "\n")

    # Bucle interactivo para recibir consultas del usuario continuamente
    while True:
        try:
            # Capturar la consulta ingresada por teclado
            query_usuario = input("👉 Ingresa tu consulta: ").strip()

            # Condición de salida del bucle
            if query_usuario.lower() in ["salir", "exit", "quit"]:
                print("\n👋 ¡Hasta luego! Cerrando el sistema RAG.")
                break

            # Validar que la consulta no esté vacía
            if not query_usuario:
                print("⚠️ Por favor, ingresa una pregunta válida.\n")
                continue

            print("\n⏳ Buscando información en ChromaDB y generando respuesta...\n")

            # Ejecutar la función asíncrona del pipeline RAG
            resultado = await get_rag_response(query_usuario)

            # Mostrar los resultados estructurados
            print("┌────────────────────────────────────────────────────────────")
            print(f"🤖 **Respuesta:** {resultado.respuesta}")
            print(f"🔍 **Encontrado en contexto?:** {'Sí ✅' if resultado.encontrado_en_contexto else 'No ❌ (Filtrado por veracidad)'}")
            print(f"📚 **Referencias:** {resultado.referencias if resultado.referencias else 'Ninguna'}")
            print("└────────────────────────────────────────────────────────────\n")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupción detectada. Saliendo del sistema RAG.")
            break
        except Exception as e:
            print(f"\n❌ Ocurrió un error al procesar la consulta: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())