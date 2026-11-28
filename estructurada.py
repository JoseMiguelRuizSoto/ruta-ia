from enum import Enum
from pydantic import BaseModel, Field
from google.genai import types
from llm import generar


# 1. El esquema: qué valores son válidos
class Categoria(str, Enum):
    RED = "red"
    FACTURACION = "facturacion"
    EQUIPO = "equipo"
    OTRO = "otro"


class Prioridad(str, Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"


class Clasificacion(BaseModel):
    categoria: Categoria
    prioridad: Prioridad
    resumen: str = Field(description="Resumen del problema en máximo 12 palabras")


# 2. Le pedimos al modelo que responda en JSON siguiendo ese esquema
config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=Clasificacion,
)

tickets = [
    "Mi internet se corta cada 10 minutos desde ayer.",
    "Desde el martes no puedo ver series en la noche, de día anda bien.",
    "Me cobraron el mes completo pero estuve 5 días sin señal.",
    "El router está echando humo y huele a quemado.",
    "Quiero saber si puedo cambiarme a un plan más barato.",
]

for i, ticket in enumerate(tickets):
    prompt = f"Eres un clasificador de tickets de soporte de una empresa de telecomunicaciones. Clasifica este ticket: {ticket}"
    try:
        resp = generar(prompt, config)
    except RuntimeError:
        print(f"(sin respuesta) {ticket}")
        continue

    if i == 0:
        print("JSON crudo del primer ticket:", resp.text, "\n")

    c = resp.parsed  # ya es un objeto Clasificacion, no texto
    print(f"{c.categoria.value:<12}{c.prioridad.value:<7}{c.resumen}")