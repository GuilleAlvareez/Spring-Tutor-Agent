# 🍃 Spring Tutor Agent

> Tutor conversacional con IA para aprender Spring Framework. Pregunta sobre Spring Boot, Spring Security, Spring Data JPA y más — el agente responde con contexto extraído de la documentación oficial usando **RAG**.

🔗 **[Demo en vivo](https://springtutoragent-production.up.railway.app)** · 📂 **[Repositorio](https://github.com/GuilleAlvareez/Spring-Tutor-Agent)**

---

![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5-6DB33F?style=flat&logo=springboot&logoColor=white)
![Angular](https://img.shields.io/badge/Angular-19-DD0031?style=flat&logo=angular&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C?style=flat)
![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=flat&logo=railway&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)

---

## ¿Qué es?

**Spring Tutor Agent** es una aplicación full-stack que combina un backend en Spring Boot, un agente de IA en Python con LangChain y un frontend en Angular para crear un tutor interactivo sobre el ecosistema Spring.

El agente usa el patrón **RAG (Retrieval-Augmented Generation)**: antes de responder, recupera los fragmentos más relevantes de la documentación oficial de Spring y los inyecta en el contexto del LLM. Esto garantiza respuestas precisas y fundamentadas en la documentación real.

---

## ✨ Funcionalidades

- 🤖 **Chat conversacional** — interfaz fluida impulsada por DeepSeek v3 vía OpenRouter
- 📚 **RAG sobre documentación oficial** — 379 chunks indexados de Spring Boot, Spring Data JPA, Spring Security y más
- 🎯 **Agente especializado** — rechaza preguntas fuera del ecosistema Spring
- 💬 **Markdown + Syntax Highlighting** — respuestas con código formateado y resaltado
- 🛡️ **Manejo de errores robusto** — excepciones personalizadas y respuestas HTTP semánticas (503, etc.)
- 🧪 **Tests unitarios** — cobertura con JUnit 5 + Mockito

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   Angular 19          Spring Boot 3.5      FastAPI  │
│   (Frontend)    ────▶  (Backend/Proxy)  ────▶ (IA)  │
│                  REST                   HTTP        │
│                                           │         │
│                                      ChromaDB       │
│                                      PostgreSQL     │
└─────────────────────────────────────────────────────┘
```

**Decisión de diseño:** Angular nunca habla directamente con el agente Python. Spring Boot actúa como proxy y capa de seguridad — el agente nunca está expuesto a internet.

---

## 🛠️ Stack tecnológico

| Capa          | Tecnología                        | Descripción                                |
| ------------- | --------------------------------- | ------------------------------------------ |
| Frontend      | Angular 19 + Tailwind CSS         | Chat UI con Markdown y syntax highlighting |
| Backend       | Spring Boot 3.5 + Java 21         | API REST + proxy al agente                 |
| Agente IA     | Python 3.12 + FastAPI + LangChain | Pipeline RAG + LLM                         |
| Vector DB     | ChromaDB                          | Almacén de embeddings                      |
| LLM           | DeepSeek v3 vía OpenRouter        | Generación de respuestas                   |
| Base de datos | PostgreSQL (Supabase)             | Persistencia de mensajes                   |
| Contenedores  | Docker + Docker Compose           | Orquestación local                         |
| Deploy        | Railway                           | Despliegue en producción                   |

---

## 🤖 Pipeline RAG

```
Pregunta del usuario
        │
        ▼
Embeddings de la pregunta
        │
        ▼
Búsqueda semántica en ChromaDB
        │
        ▼
Top 8 chunks más relevantes
        │
        ▼
Prompt enriquecido con contexto + historial
        │
        ▼
DeepSeek v3 genera la respuesta
        │
        ▼
Respuesta con Markdown al usuario
```

**Documentación indexada:**

- Spring Boot — Getting Started, Auto-configuration, Actuator
- Spring Data JPA — repositorios, entidades, queries
- Spring MVC — controllers, anotaciones REST
- Spring Security — autenticación, autorización

---

## 🚀 Ejecutar en local

### Opción 1: Docker Compose (recomendado)

```bash
git clone https://github.com/GuilleAlvareez/Spring-Tutor-Agent.git
cd Spring-Tutor-Agent

# Crear fichero de variables de entorno
cp .env.example .env   # Rellenar con tus credenciales

docker-compose up --build
```

Abre [http://localhost](http://localhost)

### Opción 2: Manual

**Requisitos:** Java 21, Python 3.12, Node.js 18+, API key de [OpenRouter](https://openrouter.ai)

```bash
# 1. Agente Python
cd agent
python -m venv venv && venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env   # Rellenar credenciales
python ingest.py       # Indexar documentación (solo la primera vez)
uvicorn main:app --reload --port 8000

# 2. Backend Spring Boot
cd backend
./mvnw spring-boot:run   # Linux/Mac
mvnw.cmd spring-boot:run # Windows

# 3. Frontend Angular
cd frontend
npm install && ng serve
```

Abre [http://localhost:4200](http://localhost:4200)

---

## 🧪 Tests

```bash
cd backend
./mvnw test
```

```
Tests run: 4, Failures: 0, Errors: 0, Skipped: 0 — BUILD SUCCESS
```

---

## 📁 Estructura del proyecto

```
Spring-Tutor-Agent/
├── frontend/                        # Angular 19
│   └── src/app/
│       ├── pages/chat/              # Componente principal del chat
│       └── services/                # Servicios HTTP
├── backend/                         # Spring Boot
│   └── src/main/java/com/springtutor/backend/
│       ├── agent/                   # Proxy + manejo de errores
│       ├── config/                  # CORS, GlobalExceptionHandler
│       ├── controller/              # Endpoints REST
│       ├── service/                 # Lógica de negocio
│       └── model/                   # Entidades JPA
└── agent/                           # Python + LangChain
    ├── app/
    │   ├── agent.py                 # Lógica RAG + LLM + system prompt
    │   ├── rag/                     # Loader, vectorstore, retriever
    │   └── config.py                # Configuración centralizada
    ├── data/                        # Documentación en Markdown
    ├── ingest.py                    # Script de indexación
    └── main.py                      # App FastAPI
```

---

## 📄 Licencia

MIT © [Guillermo Álvarez](https://github.com/GuilleAlvareez)
