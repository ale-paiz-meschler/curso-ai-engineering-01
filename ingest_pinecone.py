import os
from dotenv import load_dotenv

# 1. ¡Crucial! Cargar las variables del archivo .env antes de inicializar SDKs
load_dotenv()

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders.csv_loader import CSVLoader

def inicializar_ingesta_pinecone():
    # 1. Cargar variables de configuración desde el entorno (.env)
    api_key = os.environ.get("PINECONE_API_KEY")
    index_name = os.environ.get("PINECONE_INDEX_NAME", "ai-engineering-index")
    namespace_name = os.environ.get("PINECONE_NAMESPACE", "dberrors")
    cloud = os.environ.get("PINECONE_CLOUD", "aws")
    region = os.environ.get("PINECONE_REGION", "us-east-1")

    if not api_key:
        raise ValueError("❌ No se encontró la variable PINECONE_API_KEY en el entorno o archivo .env")

    index_name = "ai-engineering-index"
    namespace_name = "patrones-diseno"

    pc = Pinecone(api_key=api_key)

    # Asegurar que el índice Serverless exista con 1536 dimensiones (Error 1 evitado)
    if index_name not in [idx.name for idx in pc.list_indexes()]:
        print(f"☁️ Creando índice Serverless '{index_name}' en Pinecone...")
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    print("📂 Leyendo documentos de la carpeta 'data'...")
    # Carga el CSV convirtiendo cada fila en un documento con sus columnas como metadatos
    loader = CSVLoader(
        file_path="./data/dberrors.csv",
        csv_args={
            'delimiter': ',',
            'quotechar': '"',
        }
    )
    documentos = loader.load()

    # Chunking estratégico basado en tokens (Error 3 evitado: entre 500 y 800 tokens)
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=600,
        chunk_overlap=60
    )
    chunks = text_splitter.split_documents(documentos)
    print(f"✂️ Se generaron {len(chunks)} chunks optimizados.")

    # Inyectar texto original y metadatos avanzados
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
        chunk.metadata["source"] = chunk.metadata.get("source", "desconocido")
        chunk.metadata["category"] = "arquitectura"
        # Guardar el texto plano en metadatos evita llamadas a DBs externas (Punto 2 de la consigna)
        chunk.metadata["text_content"] = chunk.page_content

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    print(f"🚀 Subiendo vectores a Pinecone (Namespace: '{namespace_name}')... (Error 2 evitado)")
    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=index_name,
        namespace=namespace_name
    )
    print("✅ Ingesta en Pinecone completada con éxito.")
    return vectorstore

if __name__ == "__main__":
    inicializar_ingesta_pinecone()