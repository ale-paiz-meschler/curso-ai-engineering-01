import json
from hybrid_retriever import RAGSystem

def ejecutar_evaluacion():
    print("📊 Iniciando evaluación formal del sistema RAG (Benchmark de 5 preguntas)...\n")
    
    try:
        with open("golden_set.json", "r", encoding="utf-8") as f:
            golden_set = json.load(f)
    except FileNotFoundError:
        print("⚠️ No se encontró el archivo 'golden_set.json'.")
        return

    # Inicializar la clase RAGSystem obligatoria
    rag = RAGSystem()
    k = 5
    
    total_preguntas = len(golden_set)
    aciertos_recall = 0
    precisiones_acumuladas = 0.0

    print(f"{'PREGUNTA':<70} | {'RECALL@5':<10} | {'PRECISION@5'}")
    print("-" * 95)

    for item in golden_set:
        pregunta = item["pregunta"]
        id_esperado = item["documento_id_esperado"].lower()

        # Recuperar el Top-5 usando RAGSystem
        docs_recuperados = rag.retrieve(pregunta)
        
        # Evaluar Recall@5 (¿El relevante está en el top-k?)
        relevantes_en_top_k = 0
        encontrado_recall = False
        
        for doc in docs_recuperados[:k]:
            contenido = doc.page_content.lower()
            if id_esperado in contenido:
                relevantes_en_top_k += 1
                encontrado_recall = True

        if encontrado_recall:
            aciertos_recall += 1
            recall_item = 1.0
        else:
            recall_item = 0.0

        # Evaluar Precision@5 (Proporción de documentos útiles en el top-k recuperado)
        # Asumiendo 1 documento relevante por consulta en el benchmark
        precision_item = relevantes_en_top_k / min(len(docs_recuperados), k) if docs_recuperados else 0.0
        precisiones_acumuladas += precision_item

        print(f"{pregunta:<70} | {f'{recall_item*100:.0f}%':<10} | {f'{precision_item*100:.0f}%'}")

    # Métricas globales del sistema
    global_recall = (aciertos_recall / total_preguntas) * 100
    global_precision = (precisiones_acumuladas / total_preguntas) * 100

    print("\n" + "="*50)
    print("📈 RESUMEN DE RESULTADOS DE EVALUACIÓN RAG")
    print("="*50)
    print(f"  - Total de consultas evaluadas : {total_preguntas}")
    print(f"  - Recall@5 global             : {global_recall:.2f}%")
    print(f"  - Precision@5 global          : {global_precision:.2f}%")
    print("="*50)

if __name__ == "__main__":
    ejecutar_evaluacion()