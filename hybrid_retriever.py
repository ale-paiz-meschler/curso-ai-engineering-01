import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.retrievers import BM25Retriever
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Importación segura o alternativa para evitar el ModuleNotFoundError
try:
    from langchain.retrievers import EnsembleRetriever
except ImportError:
    from langchain_core.retrievers import BaseRetriever
    from pydantic import Field
    from typing import List
    from langchain_core.documents import Document

    class EnsembleRetriever(BaseRetriever):
        retrievers: List = Field(...)
        weights: List[float] = Field(...)

        def _get_relevant_documents(self, query: str, *, run_manager=None) -> List[Document]:
            doc_scores = {}
            for retriever, weight in zip(self.retrievers, self.weights):
                # CORRECCIÓN: Invocamos limpiamente sin duplicar run_manager
                docs = retriever.invoke(query)
                for rank, doc in enumerate(docs):
                    score = weight * (1.0 / (rank + 1))
                    if doc.page_content in doc_scores:
                        doc_scores[doc.page_content]["score"] += score
                    else:
                        doc_scores[doc.page_content] = {"doc": doc, "score": score}
            
            sorted_docs = sorted(doc_scores.values(), key=lambda x: x["score"], reverse=True)
            return [item["doc"] for item in sorted_docs[:3]]

# Este módulo combina lo mejor de dos mundos: la búsqueda semántica densa de Pinecone 
# (que entiende conceptos e intenciones) con la búsqueda léxica exacta de BM25 (perfecta 
# para nombres propios, códigos de error o términos técnicos específicos que la IA a veces confunde).
# Se utiliza un EnsembleRetriever de LangChain.
def obtener_recuperador_hibrido():
    load_dotenv()
    index_name = "ai-engineering-index"
    namespace_name = "patrones-diseno"

    # 1. Recuperador Vectorial (Pinecone)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings,
        namespace=namespace_name
    )
    vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 2. Recuperador Léxico (BM25 basado en los documentos locales)
    loader = DirectoryLoader('./data', glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=600, chunk_overlap=60)
    chunk_docs = text_splitter.split_documents(docs)

    bm25_retriever = BM25Retriever.from_documents(chunk_docs)
    bm25_retriever.k = 3

    # 3. Combinación Híbrida robusta
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.4, 0.6]
    )

    return ensemble_retriever

if __name__ == "__main__":
    retriever = obtener_recuperador_hibrido()
    resultados = retriever.invoke("ORA-00942 table or view does not exist")
    print(f"✅ Recuperador híbrido funcionando. Documentos encontrados: {len(resultados)}")