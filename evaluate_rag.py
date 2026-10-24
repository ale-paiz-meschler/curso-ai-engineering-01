import json
from hybrid_retriever import obtener_recuperador_hibrido

def evaluar_sistema_rag():
    print("📊 Iniciando evaluación local del RAG con Golden Set...\n")
    
    try:
        with open("golden_set.json", "r", encoding="utf-8") as f:
            golden_set = json.load(f)
    except FileNotFoundError:
        print("⚠️ No se encontró el archivo 'golden_set.json'. Asegúrate de crearlo.")
        return

    retriever = obtener_recuperador_hibrido()
    k = 5  # Top-k a evaluar
    
    aciertos_totales = 0
    total_preguntas = len(golden_set)

    for item in golden_set:
        pregunta = item["pregunta"]
        id_esperado = item["documento_id_esperado"].lower() # Ej: "mssql", "oracle", etc.

        # Recuperar documentos para la pregunta
        docs_recuperados = retriever.invoke(pregunta)
        
        # Verificar si el identificador esperado (o palabra clave del motor/error) 
        # se encuentra en el contenido del texto recuperado (page_content)
        encontrado = False
        for doc in docs_recuperados[:k]:
            contenido = doc.page_content.lower()
            
            # Validamos si el identificador esperado (ej. mssql, oracle) 
            # o palabras clave específicas están en el chunk recuperado
            if id_esperado in contenido:
                encontrado = True
                break
        
        if encontrado:
            aciertos_totales += 1
            print(f"✅ Pregunta: '{pregunta}' -> ENCONTRADO en el Top-{k}")
        else:
            print(f"❌ Pregunta: '{pregunta}' -> NO ENCONTRADO en el Top-{k}")

    precision_at_k = aciertos_totales / total_preguntas
    recall_at_k = aciertos_totales / total_preguntas

    print("\n" + "="*40)
    print("📈 RESULTADOS DE LA EVALUACIÓN RAG")
    print("="*40)
    print(f"  - Total de consultas evaluadas: {total_preguntas}")
    print(f"  - Precision@{k}: {precision_at_k * 100:.2f}%")
    print(f"  - Recall@{k}: {recall_at_k * 100:.2f}%")
    print("="*40)

if __name__ == "__main__":
    evaluar_sistema_rag()