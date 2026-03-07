# Spring Tutor Agent — Agente IA

Agente de inteligencia artificial del proyecto Spring Tutor Agent. Construido con Python, FastAPI y LangChain. Implementa un sistema RAG (Retrieval-Augmented Generation) que combina documentación local en Markdown con scraping de la documentación oficial de Spring para responder preguntas con contexto real.

---

## Stack

| Tecnología       | Versión | Rol                     |
| ---------------- | ------- | ----------------------- |
| Python           | 3.11+   | Lenguaje                |
| FastAPI          | Latest  | API REST                |
| Uvicorn          | Latest  | Servidor ASGI           |
| LangChain        | Latest  | Framework del agente    |
| LangChain OpenAI | Latest  | Conector LLM            |
| ChromaDB         | Latest  | Base de datos vectorial |
| BeautifulSoup4   | Latest  | Web scraping            |
| python-dotenv    | Latest  | Variables de entorno    |

---

## Estructura del proyecto

```
agent/
├── main.py                  → arranca FastAPI y define los endpoints
├── ingest.py                → script de indexación (se ejecuta una vez)
├── requirements.txt         → dependencias
├── .env                     → credenciales (no se sube a git)
├── .env.example             → plantilla de credenciales
├── data/                    → archivos .md con documentación local
│   ├── spring-basics.md
│   ├── spring-annotations.md
│   ├── spring-data-jpa.md
│   └── spring-rest.md
├── app/
│   ├── agent.py             → lógica principal: RAG + LLM
│   ├── config.py            → variables de configuración centralizadas
│   └── rag/
│       ├── loader.py        → carga y trocea los .md de data/
│       ├── vectorstore.py   → gestiona ChromaDB
│       ├── retriever.py     → busca chunks relevantes para una pregunta
│       └── scraper.py       → descarga documentación oficial de Spring
└── chroma_db/               → base de datos vectorial (generada automáticamente)
```

### ¿Por qué esta estructura?

Cada archivo tiene una única responsabilidad:

- **`main.py`** — solo define endpoints HTTP, no contiene lógica
- **`app/agent.py`** — orquesta el flujo completo: RAG + LLM
- **`app/config.py`** — punto único de configuración, equivalente al `application.properties` de Spring
- **`app/rag/loader.py`** — solo sabe leer y trocear archivos
- **`app/rag/vectorstore.py`** — solo sabe guardar y recuperar de ChromaDB
- **`app/rag/retriever.py`** — solo sabe buscar chunks relevantes
- **`app/rag/scraper.py`** — solo sabe descargar páginas web

---

## ¿Qué es RAG?

RAG (Retrieval-Augmented Generation) es un patrón que mejora las respuestas del LLM añadiéndole contexto relevante antes de generar la respuesta.

Sin RAG el LLM responde solo con su conocimiento de entrenamiento, que puede estar desactualizado. Con RAG el LLM responde basándose en documentación real y actualizada.

```
Sin RAG:
Pregunta → LLM → Respuesta (basada en entrenamiento)

Con RAG:
Pregunta → ChromaDB (busca docs relevantes) → LLM (con contexto) → Respuesta
```

---

## Flujo completo de una petición

```
Spring Boot → POST /chat {"message": "¿Qué es @Autowired?"}
                    |
                    ↓
             main.py recibe la petición
                    |
                    ↓
             agent.py orquesta el flujo
                    |
          ┌─────────┴──────────┐
          ↓                    ↓
   retriever.py          config.py
   busca en ChromaDB     (parámetros)
   los 8 chunks más
   relevantes
          |
          ↓
   Construye el prompt:
   "Contexto: [chunk1, chunk2...]
    Pregunta: ¿Qué es @Autowired?"
          |
          ↓
   LLM (DeepSeek via OpenRouter)
   genera la respuesta con contexto
          |
          ↓
Spring Boot ← {"response": "@Autowired es..."}
```

---

## Endpoints

### GET `/health`

Comprueba que el agente está activo.

**Respuesta:**

```json
{ "status": "Agent is running!" }
```

### POST `/chat`

Recibe un mensaje y devuelve la respuesta del agente con RAG.

**Body:**

```json
{ "message": "¿Qué hace la anotación @Service?" }
```

**Respuesta:**

```json
{ "response": "@Service es una especialización de @Component..." }
```

---

## Sistema RAG — Cómo funciona por dentro

### 1. Ingesta (ingest.py)

Se ejecuta una sola vez para poblar ChromaDB. Combina dos fuentes:

**Archivos locales** — lee todos los `.md` de `data/`, los trocea en chunks de 1000 caracteres con 200 de solapamiento y los indexa en ChromaDB.

**Web scraping** — descarga páginas de la documentación oficial de Spring, limpia el HTML y los trocea e indexa igual que los archivos locales.

```bash
python ingest.py
```

### 2. Embeddings

Un embedding convierte texto en un vector numérico que representa su significado semántico. Textos con significado similar tienen vectores similares aunque usen palabras distintas.

```
"¿Qué es @Autowired?"  →  [0.23, -0.45, 0.12, ...]  (vector de 1536 dimensiones)
```

Se usa el modelo `text-embedding-3-small` de OpenAI a través de OpenRouter.

### 3. ChromaDB

Base de datos vectorial que guarda los chunks junto con sus embeddings. Cuando se hace una búsqueda, ChromaDB convierte la pregunta en un vector y devuelve los chunks cuyos vectores son más cercanos — es decir, los más relevantes semánticamente.

### 4. Retriever

Busca los 8 chunks más relevantes para la pregunta del usuario y los concatena en un único texto de contexto que se inyecta en el prompt del LLM.

---

## Fuentes de documentación

### Fase 1 (implementada)

- Archivos `.md` locales en `data/` con conceptos básicos de Spring
- Documentación oficial de Spring Boot (getting started, using, application properties)
- Documentación oficial de Spring Data JPA

### Fase 2 (pendiente)

- Documentación oficial de Spring Security (cuando se implemente la autenticación)

### Fase 3 (pendiente)

- Documentación oficial de Spring Framework core

Para añadir nuevas fuentes basta con añadir URLs al array `SPRING_DOCS_URLS` en `scraper.py` o añadir archivos `.md` a `data/` y volver a ejecutar `ingest.py`.

---

## Configuración

Todas las variables de configuración están centralizadas en `app/config.py`:

```python
LLM_MODEL = "deepseek/deepseek-v3-0324"   # modelo LLM
TOP_K_RESULTS = 8      # chunks recuperados por pregunta
CHUNK_SIZE = 1000      # tamaño máximo de cada chunk en caracteres
CHUNK_OVERLAP = 200    # solapamiento entre chunks
```

El archivo `.env` contiene las credenciales:

```
OPENROUTER_API_KEY=tu_api_key
```

Usa `.env.example` como plantilla.

---

## Arrancar el agente

**Requisitos previos:**

- Python 3.11+
- Una API key de OpenRouter

**Pasos:**

1. Crea y activa el entorno virtual:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Copia `.env.example` a `.env` y añade tu API key

4. Indexa la documentación (solo la primera vez o cuando añadas docs nuevas):

```bash
python ingest.py
```

5. Arranca el agente:

```bash
uvicorn main:app --reload --port 8000
```

El agente estará disponible en `http://localhost:8000`.

---

## Próximos pasos

- [ ] Añadir documentación de Spring Security (Fase 2)
- [ ] Implementar historial de conversación en el contexto del agente
- [ ] Añadir más archivos `.md` locales con casos de uso avanzados
- [ ] Optimizar el tamaño de chunks para mejores resultados
- [ ] Dockerizar el agente
