from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, SecretStr, field_validator

from enum import Enum
from typing import List
from pydantic import BaseModel, Field, field_validator

class NivelCriticidad(str, Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"

class ExtractedTechnicalEntities(BaseModel):
    tecnologías: List[str] = Field(
        description="Lista de tecnologías, lenguajes, frameworks o herramientas de infraestructura detectadas en el texto."
    )
    nivel_de_criticidad: NivelCriticidad = Field(
        description="Nivel de criticidad estimado del reporte o arquitectura descrita."
    )
    resumen_tecnico: str = Field(
        description="Breve resumen ejecutivo técnico de una o dos líneas sobre el problema o arquitectura analizada."
    )

    @field_validator("tecnologías")
    @classmethod
    def validar_tecnologias_no_vacias(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("La lista de tecnologías extraídas no puede estar vacía.")
        return [t.strip() for t in v if t.strip()]

class Provider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"

class ChatMessage(BaseModel):
    role: str = Field(description="'user', 'assistant' o 'system'")
    content: str

    @field_validator("role")
    @classmethod
    def rol_valido(cls, v: str) -> str:
        roles_permitidos = {"user", "assistant", "system"}
        if v not in roles_permitidos:
            raise ValueError(f"role debe ser uno de {roles_permitidos}, recibido: '{v}'")
        return v

class LLMConfig(BaseModel):
    provider: Provider
    model: str
    openai_api_key: Optional[SecretStr] = None
    anthropic_api_key: Optional[SecretStr] = None
    google_api_key: Optional[SecretStr] = None
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=1024, gt=0)

class ModelResponse(BaseModel):
    provider: Provider
    model: str
    content: str
    error: Optional[str] = None

from pydantic import ValidationError