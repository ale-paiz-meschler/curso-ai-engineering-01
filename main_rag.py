import asyncio
from ingest import inicializar_base_vectorial
from rag_chain import get_rag_response

async def main():
    print("🚀 Inicializando el Sistema RAG End-to-End...\n")

    # Paso 1: Inicializar / Cargar la base vectorial
    inicializar_base_vectorial()

    print("\n" + "="*70)
    print("🧪 EJECUCIÓN DE PRUEBAS OBLIGATORIAS (EVIDENCIA DE NO ALUCINACIÓN)")
    print("="*70)

    # --- PRUEBA 1: Pregunta respondida por los documentos ---
    pregunta_valida = "¿Cuáles son los aspectos fundamentales o características del patrón documentado?"
    print(f"\n👉 [PRUEBA 1 - Válida] Consultando: '{pregunta_valida}'")
    
    res_valida = await get_rag_response(pregunta_valida)
    print(f"   🤖 Respuesta del Modelo: {res_valida.respuesta}")
    print(f"   🔍 Encontrado en contexto?: {res_valida.encontrado_en_contexto}")
    print(f"   📚 Referencias utilizadas: {res_valida.referencias}")

    # --- PRUEBA 2: Pregunta Trampa (Fuera de contexto) ---
    pregunta_trampa = "¿Quién ganó la medalla de oro en maratón en los Juegos Olímpicos de París 2024?"
    print(f"\n👉 [PRUEBA 2 - Trampa] Consultando: '{pregunta_trampa}'")
    
    res_trampa = await get_rag_response(pregunta_trampa)
    print(f"   🤖 Respuesta del Modelo (Anti-alucinación): {res_trampa.respuesta}")
    print(f"   🔍 Encontrado en contexto?: {res_trampa.encontrado_en_contexto}")
    print(f"   📚 Referencias utilizadas: {res_trampa.referencias}")

    print("\n" + "="*70)
    print("💬 MODO INTERACTIVO (Escribe 'salir' para terminar)")
    print("="*70 + "\n")

    # Bucle interactivo opcional para continuar probando
    while True:
        try:
            query_usuario = input("👉 Ingresa tu consulta: ").strip()
            if query_usuario.lower() in ["salir", "exit", "quit"]:
                print("\n👋 ¡Hasta luego!")
                break
            if not query_usuario:
                continue

            print("\n⏳ Procesando consulta...\n")
            resultado = await get_rag_response(query_usuario)
            print("┌────────────────────────────────────────────────────────────")
            print(f"🤖 **Respuesta:** {resultado.respuesta}")
            print(f"🔍 **Encontrado en contexto?:** {'Sí ✅' if resultado.encontrado_en_contexto else 'No ❌ (Filtrado)'}")
            print(f"📚 **Referencias:** {resultado.referencias if resultado.referencias else 'Ninguna'}")
            print("└────────────────────────────────────────────────────────────\n")

        except KeyboardInterrupt:
            print("\n\n👋 Saliendo del sistema.")
            break

if __name__ == "__main__":
    asyncio.run(main())