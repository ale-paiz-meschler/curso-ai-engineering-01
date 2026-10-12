import asyncio
from pipeline import process_text

async def main():
    print("🚀 Iniciando pipeline de extracción asíncrona...\n")

    # --- Caso de prueba 1: texto claro y estructurado ---
    texto_claro = (
        "El microservicio de pagos desarrollado en Java con Spring Boot presenta fallas intermitentes "
        "al conectar con la base de datos MySQL desplegada en un clúster de Kubernetes en Google Cloud Run. "
        "El incidente genera pérdida de transacciones y requiere atención urgente."
    )

    print("--- CASO 1: Texto técnico claro ---")
    try:
        resultado_1 = await process_text(texto_claro)
        print("✅ Extracción exitosa:")
        print(f"  - Tecnologías: {resultado_1.tecnologías}")
        print(f"  - Criticidad: {resultado_1.nivel_de_criticidad}")
        print(f"  - Resumen: {resultado_1.resumen_tecnico}\n")
    except Exception as e:
        print(f"❌ Error controlado en validación: {e}\n")

    # --- Caso de prueba 2 (prueba de estrés): Texto ambiguo o escaso ---
    # Esto cumple con el punto de evaluar cómo reacciona el validador/modelo ante la ambigüedad
    texto_ambiguo = "El sistema falló hoy."

    print("--- CASO 2: Prueba de estrés (texto ambiguo) ---")
    try:
        resultado_2 = await process_text(texto_ambiguo)
        print("✅ Resultado del texto ambiguo:")
        print(f"  - Tecnologías: {resultado_2.tecnologías}")
        print(f"  - Criticidad: {resultado_2.nivel_de_criticidad}")
        print(f"  - Resumen: {resultado_2.resumen_tecnico}\n")
    except Exception as e:
        print(f"⚠️ El validador o el pipeline reaccionó ante la ambigüedad/fallas de esquema: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())