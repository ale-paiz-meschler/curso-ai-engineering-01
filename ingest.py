import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

def inicializar_base_vectorial():
    persist_dir = "./vectorstore"
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    if os.path.exists(persist_dir) and os.listdir(persist_dir):
        print("📂 [Optimización] La base vectorial ya existe en './vectorstore'. Omitiendo reingesta.")
        return Chroma(persist_directory=persist_dir, embedding_function=embeddings)

    print("📂 Leyendo archivos MD de la carpeta 'data'...")
    loader = DirectoryLoader(
        './data', 
        glob="**/*.md", 
        loader_cls=TextLoader, 
        loader_kwargs={'encoding': 'utf-8'}
    )
    documentos = loader.load()
    print(f"📄 Se cargaron {len(documentos)} documentos.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documentos)
    print(f"✂️ Se generaron {len(chunks)} fragmentos (chunks).")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    print("✅ Base vectorial ChromaDB poblada y persistida exitosamente.")
    return vectorstore