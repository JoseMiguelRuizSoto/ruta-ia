import os
import time
import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
cliente = genai.Client(http_options=types.HttpOptions(timeout=30_000))  # 30 segundos (en milisegundos)

def generar(prompt, config=None, intentos=4):
    """Llama a Gemini con reintentos ante errores temporales del servidor."""
    espera = 2
    for i in range(1, intentos + 1):
        try:
            return cliente.models.generate_content(model=GEMINI_MODEL, contents=prompt, config=config)
        except (errors.ServerError, httpx.TimeoutException) as e:
            if i == intentos:
                break  # último intento: no tiene sentido esperar
            print(f"  Intento {i}: sin respuesta del servidor ({type(e).__name__}). Reintento en {espera} s...")
            time.sleep(espera)
            espera *= 2
    raise RuntimeError("Gemini no respondió después de varios intentos")