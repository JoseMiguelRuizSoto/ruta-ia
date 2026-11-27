import os
import time
from google.genai import errors
from dotenv import load_dotenv
from google import genai
import ollama

load_dotenv()
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
cliente = genai.Client()

def generar_con_reintentos(prompt, intentos=4):
    espera = 2  # segundos
    for i in range(1, intentos + 1):
        try:
            return cliente.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        except errors.ServerError as e:  # errores 5xx: el problema es del servidor
            print(f"Intento {i}: servidor ocupado ({e.code}). Reintento en {espera} s...")
            time.sleep(espera)
            espera *= 2  # 2, 4, 8, 16...
    raise RuntimeError("Gemini no respondió después de varios intentos")

# --- Parte 1: el mismo contenido, distintos tokens ---
textos = {
    "español": "Mi internet se corta cada 10 minutos desde ayer y ya reinicié el router dos veces.",
    "inglés": "My internet drops every 10 minutes since yesterday and I already restarted the router twice.",
    "código SQL": "SELECT id, estado FROM tickets WHERE prioridad = 'alta';",
    "números": "Cliente 11.111.111-1, boleta N° 000123456, monto $45.990",
}

print(f"{'Texto':<12}{'Caracteres':>12}{'Gemini':>10}{'Llama':>10}")
for nombre, texto in textos.items():
    t_gemini = cliente.models.count_tokens(model=GEMINI_MODEL, contents=texto).total_tokens
    # raw=True: cuenta solo tu texto, sin la plantilla de chat; num_predict=1: casi no genera
    r = ollama.generate(model=OLLAMA_MODEL, prompt=texto, raw=True, options={"num_predict": 1})
    t_llama = r["prompt_eval_count"]
    print(f"{nombre:<12}{len(texto):>12}{t_gemini:>10}{t_llama:>10}")

# --- Parte 2: cuánto cuesta una llamada real ---
pregunta = "Clasifica este ticket en una palabra (red, facturación u otro): " + textos["español"]
resp = generar_con_reintentos(pregunta)
uso = resp.usage_metadata

entrada = uso.prompt_token_count or 0
salida = uso.candidates_token_count or 0
pensamiento = uso.thoughts_token_count or 0

print("\nRespuesta:", resp.text.strip())
print(f"Tokens de entrada: {entrada}")
print(f"Tokens de salida: {salida}")
print(f"Tokens de razonamiento interno: {pensamiento}")

# Precios DE EJEMPLO en USD por millón de tokens (los reales cambian; revisa la página de precios)
PRECIO_ENTRADA = 0.50
PRECIO_SALIDA = 3.00  # el razonamiento interno se cobra como salida

costo = (entrada * PRECIO_ENTRADA + (salida + pensamiento) * PRECIO_SALIDA) / 1_000_000
print(f"Costo por ticket: USD {costo:.6f}")
print(f"Costo por 10.000 tickets al día durante un mes: USD {costo * 10_000 * 30:,.2f}")