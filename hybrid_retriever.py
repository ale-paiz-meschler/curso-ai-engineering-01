import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.retrievers import BM25Retriever
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
                docs = retriever.invoke(query)
                for rank, doc in enumerate(docs):
                    score = weight * (1.0 / (rank + 1))
                    if doc.page_content in doc_scores:
                        doc_scores[doc.page_content]["score"] += score
                    else:
                        doc_scores[doc.page_content] = {"doc": doc, "score": score}
            
            sorted_docs = sorted(doc_scores.values(), key=lambda x: x["score"], reverse=True)
            return [item["doc"] for item in sorted_docs[:5]]  # Top-5 por defecto

class RAGSystem:
    """Clase que encapsula el sistema de recuperación híbrida (Pinecone + BM25)."""
    def __init__(self):
        load_dotenv()
        self.index_name = os.environ.get("PINECONE_INDEX_NAME", "ai-engineering-index")
        self.namespace_name = os.environ.get("PINECONE_NAMESPACE", "dberrors")
        
        # 1. Recuperador Vectorial (Pinecone)
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        vectorstore = PineconeVectorStore.from_existing_index(
            index_name=self.index_name,
            embedding=embeddings,
            namespace=self.namespace_name
        )
        # Configurar k=5 tal como pide la consigna
        self.vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

        # 2. Recuperador Léxico (BM25)
        loader = CSVLoader(file_path="./data/dberrors.csv", csv_args={'delimiter': ',', 'quotechar': '"'})
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=600, chunk_overlap=60)
        chunk_docs = text_splitter.split_documents(docs)

        self.bm25_retriever = BM25Retriever.from_documents(chunk_docs)
        self.bm25_retriever.k = 5

        # 3. EnsembleRetriever Híbrido (40% BM25, 60% Vectorial)
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.bm25_retriever, self.vector_retriever],
            weights=[0.4, 0.6]
        )

    def retrieve(self, query: str):
        """Recibe una consulta y devuelve los top-5 documentos combinados."""
        return self.ensemble_retriever.invoke(query)

if __name__ == "__main__":
    rag = RAGSystem()
    resultados = rag.retrieve("Error 2627 SQL Server")
    print(f"✅ RAGSystem probado con éxito. Documentos recuperados (Top-5): {len(resultados)}")