import os
from dotenv import load_dotenv
from google import genai
import ollama

load_dotenv()  # lee las variables desde .env

GEMINI_MODEL = os.getenv("GEMINI_MODEL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

pregunta = "Explica en una frase qué es un token en un LLM."

# Modelo en la nube (Gemini, plan gratuito)
cliente = genai.Client()
respuesta = cliente.models.generate_content(model=GEMINI_MODEL, contents=pregunta)
print(f"Gemini ({GEMINI_MODEL}):", respuesta.text)

# Modelo local (Ollama)
local = ollama.chat(model=OLLAMA_MODEL, messages=[{"role": "user", "content": pregunta}])
print(f"Ollama ({OLLAMA_MODEL}):", local["message"]["content"])