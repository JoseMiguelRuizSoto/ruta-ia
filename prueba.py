from dotenv import load_dotenv
from google import genai
import ollama

load_dotenv()  # lee GEMINI_API_KEY desde .env

pregunta = "Explica en una frase qué es un token en un LLM."

# Modelo en la nube (Gemini, plan gratuito)
cliente = genai.Client()
respuesta = cliente.models.generate_content(model="gemini-2.5-flash", contents=pregunta)
print("Gemini:", respuesta.text)

# Modelo local (Ollama)
local = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": pregunta}])
print("Ollama:", local["message"]["content"])