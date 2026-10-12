from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Corpus mejorado con vocabulario diverso (sin repetición excesiva de keywords exactas)
corpus = [
    "Informe de un estudiante sobre los contrastes estructurales entre arquitecturas de servicios distribuidos y sistemas monolíticos tradicionales.", # Oración 1
    "Hallazgos arqueológicos y restos de estructuras megalíticas descubiertos en territorio mexicano durante septiembre de 2026.", # Oración 2
    "Consideraciones técnicas para orquestar contenedores con Kubernetes utilizando entornos basados en Quarkus.", # Oración 3
    "Las rutinas de alta intensidad basadas en estaciones múltiples y circuitos de Crossfit.", # Oración 4
    "Dificultades operativas al migrar cargas de trabajo contenedorizadas hacia plataformas como OpenShift o equivalentes.", # Oración 5
    "Guía para exponer endpoints REST escalables en infraestructuras Cloud.", # Oración 6
    "Comparativa de rendimiento y características entre Spring Boot y frameworks nativos para la nube." # Oración 7
]

print("=== SISTEMA DE RECUPERACIÓN Y SIMILITUD COSENO (TF-IDF) ===")

# 2. Entrada interactiva de la query
query_usuario = input("👉 Ingrese su consulta de búsqueda (query): ").strip()

if not query_usuario:
    print("❌ Error: La consulta no puede estar vacía.")
else:
    query = [query_usuario]

    # 3. Vectorización de textos (Pipeline TF-IDF)
    vectorizer = TfidfVectorizer()
    matriz_corpus = vectorizer.fit_transform(corpus)
    vector_query = vectorizer.transform(query)

    # 4. Cálculo de Similitud Coseno
    similitudes = cosine_similarity(vector_query, matriz_corpus)

    # 5. Ranking y visualización con numeración cruzada exacta
    print(f"\n--- RESULTADOS DE RECUPERACIÓN PARA: '{query_usuario}' ---")
    
    # Emparejar el índice con su respectivo puntaje y ordenar de mayor a menor (Ranking)
    resultados_ordenados = sorted(
        enumerate(similitudes[0]), 
        key=lambda x: x[1], 
        reverse=True
    )

    for rank, (idx, score) in enumerate(resultados_ordenados, start=1):
        print(f"{rank}° Lugar -> [Oración {idx + 1}] (Score: {score:.4f}): {corpus[idx]}")
