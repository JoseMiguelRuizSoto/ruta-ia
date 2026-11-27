from google.genai import types
from llm import generar

CATEGORIAS = "red, facturación, equipo u otro"

tickets = {
    "explícito": "Mi internet se corta cada 10 minutos desde ayer.",
    "implícito": "Desde el martes no puedo ver series en la noche, de día anda bien.",
    "ambiguo": "Me cobraron el mes completo pero estuve 5 días sin señal.",
}

modos = {
    "normal": None,  # el modelo decide cuánto razonar
    "bajo": types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low")
    ),
}

print(f"{'Ticket':<12}{'Modo':<8}{'Razonamiento':>14}  Respuesta")
for nombre, ticket in tickets.items():
    for modo, config in modos.items():
        prompt = f"Clasifica este ticket en una sola palabra ({CATEGORIAS}): {ticket}"
        try:
            resp = generar(prompt, config)
        except RuntimeError:
            print(f"{nombre:<12}{modo:<8}{'-':>14}  (sin respuesta)")
            continue
        pensamiento = resp.usage_metadata.thoughts_token_count or 0
        print(f"{nombre:<12}{modo:<8}{pensamiento:>14}  {resp.text.strip()}")