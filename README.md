# 🍃 Spring Tutor Agent

Aplicación web full-stack para aprender **Spring Framework** mediante un tutor conversacional con IA. Haz preguntas sobre Spring Boot, Spring Data JPA, anotaciones, y más — el agente responde usando contexto extraído de la documentación oficial mediante **RAG (Retrieval-Augmented Generation)**.

---

## ✨ Funcionalidades

- 🤖 **Chat con tutor IA** — interfaz conversacional impulsada por DeepSeek v3 vía OpenRouter
- 📚 **RAG sobre docs de Spring** — recupera los chunks más relevantes de la documentación antes de cada respuesta
- 💬 **Renderizado Markdown** — bloques de código, tablas y explicaciones formateadas
<!-- - 🗄️ **Persistencia de mensajes** — guardados en PostgreSQL vía Supabase -->

---

## 🏗️ Arquitectura

```
Angular (4200)
      ↕ HTTP/REST
Spring Boot (8080)   ← API + proxy
      ↕ HTTP interno
Python FastAPI (8000) ← LangChain + RAG
      ↕
ChromaDB  +  PostgreSQL (Supabase)
```

Angular solo habla con Spring Boot. Spring Boot hace de proxy hacia el agente Python. El agente nunca está expuesto directamente a internet.

---

## 🛠️ Stack tecnológico

| Capa      | Tecnología                        | Puerto  |
| --------- | --------------------------------- | ------- |
| Frontend  | Angular 19 + Tailwind CSS         | 4200    |
| Backend   | Spring Boot 3.5 + Java 21         | 8080    |
| Agente IA | Python 3.12 + FastAPI + LangChain | 8000    |
| Vector DB | ChromaDB                          | interno |
| LLM       | DeepSeek v3 vía OpenRouter        | —       |

---

## 🤖 Pipeline RAG

1. La documentación oficial de Spring se scrapea, se divide en chunks y se indexa en ChromaDB con embeddings
2. Cuando el usuario pregunta, se recuperan los 8 chunks más relevantes
3. Esos chunks se inyectan en el prompt junto con el historial de la conversación
4. El LLM genera la respuesta con ese contexto

**Fuentes indexadas:**

- Spring Boot — Getting Started y features principales
- Spring Data JPA — documentación de referencia
- Anotaciones de Spring, REST y más

---

## 🚀 Cómo ejecutarlo

### Requisitos

- Java 21
- Python 3.12
- Node.js 18+
- API key de [OpenRouter](https://openrouter.ai)

### 1. Clonar el repositorio

```bash
git clone https://github.com/GuilleAlvareez/Spring-Tutor-Agent.git
cd Spring-Tutor-Agent
```

### 2. Agente Python

```bash
cd agent
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

cp .env.example .env         # Rellenar credenciales

python ingest.py             # Indexar documentación (solo una vez)
uvicorn main:app --reload --port 8000
```

### 3. Backend Spring Boot

```bash
cd backend
# Copiar y rellenar credenciales
cp src/main/resources/application.properties.example src/main/resources/application.properties

mvnw.cmd spring-boot:run     # Windows
./mvnw spring-boot:run       # Linux/Mac
```

### 4. Frontend Angular

```bash
cd frontend
npm install
ng serve
```

Abre [http://localhost:4200](http://localhost:4200)

---

## 📁 Estructura del proyecto

```
Spring-Tutor-Agent/
├── frontend/               # Angular 19
│   └── src/app/
│       ├── pages/chat/     # Componente del chat
│       └── services/       # Servicios HTTP
├── backend/                # Spring Boot
│   └── src/main/java/com/springtutor/backend/
│       ├── agent/          # Proxy hacia el agente Python
│       ├── controller/     # Endpoints REST
│       ├── service/        # Lógica de negocio
│       ├── model/          # Entidades JPA
│       └── config/         # CORS, seguridad
└── agent/                  # Python + LangChain
    ├── app/
    │   ├── agent.py        # Lógica RAG + LLM
    │   ├── rag/            # Loader, vectorstore, retriever
    │   └── config.py       # Configuración centralizada
    ├── data/               # Documentación local en markdown
    ├── ingest.py           # Script de indexación
    └── main.py             # App FastAPI
```

---

## 📄 Licencia

MIT
