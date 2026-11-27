# Conceptos — Ruta IA Engineer

## Fase 1 · Fundamentos de LLM

### El modelo no aprende entre llamadas
Sus pesos quedan fijos después del entrenamiento. Cada llamada a la API es independiente:
no recuerda nada salvo lo que yo le envíe en el prompt (por eso existen el historial y el RAG).

### Token
Fragmento de texto que procesa el modelo (una palabra, un pedazo de palabra, un dígito).
Las APIs cobran por token, y la ventana de contexto se mide en tokens.

### Tokenizador
Corta el texto en tokens, y cada modelo lo hace a su manera.
- Mis datos: el mismo ticket usa 22 tokens en español y 19 en inglés (Gemini).
- Los números son caros: 56 caracteres de RUT y montos = 39 tokens en Gemini y 26 en Llama.
- El código es barato: 56 caracteres de SQL = 13 tokens.

### Tokens de entrada, de salida y de razonamiento
- Entrada: lo que envío. Es el más barato.
- Salida: lo que responde. Cuesta varias veces más.
- Razonamiento interno: lo que el modelo "piensa" antes de responder. No lo veo, pero se cobra como salida.
- Mis datos: para responder "Red" usó 1 token de salida y 171 de razonamiento (96 % del costo).
  Sin razonamiento, el mes bajaría de USD 160 a unos USD 7 (precios de ejemplo).

### Errores 4xx vs. 5xx
- 4xx: el error es mío (404 modelo inexistente, 401 clave inválida). NO reintentar: hay que corregir.
- 5xx: el error es del servidor (503 saturado). SÍ reintentar, porque suele ser temporal.

### Backoff exponencial
Reintentar esperando cada vez el doble (2, 4, 8 segundos...) para no saturar más al servidor.

### Timeout
Tiempo máximo que espero a un servicio externo antes de cortar. Sin timeout, mi programa
puede quedarse colgado indefinidamente (me pasó: 15 minutos esperando a Gemini).

### Configuración fuera del código (.env)
Claves y nombres de modelos van en .env, que nunca se sube a Git. Si un modelo se retira,
cambio una línea de configuración, no el código.

## Preguntas de repaso
1. ¿Por qué un ticket en español cuesta más que en inglés?
2. ¿Qué tipo de token pesó más en el costo y cómo lo reduzco?
3. ¿Cuándo reintento una llamada y cuándo no?
4. ¿Por qué el modelo no recuerda la conversación anterior?
5. ¿Qué pasa si no pongo timeout a una llamada externa?