from typing import List
from pydantic import BaseModel, Field
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# Esquema Pydantic con texto, referencias y validación de contexto
class RAGResponse(BaseModel):
    respuesta: str = Field(description="Respuesta generada basada estrictamente en el contexto recuperado.")
    referencias: List[str] = Field(description="Lista de fuentes o nombres de archivos de los documentos utilizados.")
    encontrado_en_contexto: bool = Field(description="True si la respuesta está en el contexto, False si se indicó que no se sabe.")

async def get_rag_response(query: str) -> RAGResponse:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma(
        persist_directory="./vectorstore", 
        embedding_function=embeddings
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    docs_recuperados = retriever.invoke(query)
    contexto = "\n\n".join([doc.page_content for doc in docs_recuperados])
    
    referencias = [doc.metadata.get("source", "Documento local .md") for doc in docs_recuperados]

    # 3. Parser y Prompt de Veracidad
    parser = PydanticOutputParser(pydantic_object=RAGResponse)

    system_prompt = (
        "Eres un asistente técnico experto en arquitectura de software y patrones de diseño.\n"
        "Tu objetivo es responder a la consulta del usuario utilizando ÚNICAMENTE la información provista en el CONTEXTO.\n"
        "REGLA CRÍTICA: Si la respuesta a la pregunta no se encuentra de forma explícita en el contexto, "
        "debes responder amablemente que no dispones de esa información, estableciendo 'encontrado_en_contexto' en falso "
        "y dejando la lista de referencias vacía. No inventes información.\n\n"
        "CONTEXTO RECUPERADO:\n{context}\n\n"
        "{format_instructions}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Pregunta del usuario: {query}")
    ])

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | model | parser

    # 4. Llamada asíncrona al LLM (.ainvoke)
    resultado = await chain.ainvoke({
        "context": contexto,
        "query": query,
        "format_instructions": parser.get_format_instructions()
    })

    # Asignar las referencias extraídas al modelo Pydantic
    resultado.referencias = list(set(referencias)) # Eliminar duplicados si los hay
    return resultado