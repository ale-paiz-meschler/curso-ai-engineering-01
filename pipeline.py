import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from schemas import ExtractedTechnicalEntities

load_dotenv()

def crear_pipeline_con_resiliencia():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un arquitecto de software experto. Extrae entidades técnicas estrictamente según el esquema."),
        ("user", "Analiza el siguiente texto técnico:\n\n{texto_entrada}")
    ])

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    cadena = prompt | model.with_structured_output(ExtractedTechnicalEntities)
    
    # Se añade resiliencia
    return cadena.with_retry(stop_after_attempt=3)

# Función asíncrona
async def process_text(text: str) -> ExtractedTechnicalEntities:
    pipeline = crear_pipeline_con_resiliencia()
    print(f"🔄 [LOG] Iniciando procesamiento asíncrono (.ainvoke) para el texto...")
    
    # Invocación asíncrona usando .ainvoke()
    resultado = await pipeline.ainvoke({"texto_entrada": text})
    
    print(f"✅ [LOG] Procesamiento finalizado con éxito.")
    return resultado