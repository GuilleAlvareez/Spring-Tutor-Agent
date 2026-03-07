from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.rag.retriever import get_relevant_context
from app.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, LLM_MODEL

# Configura el LLM
llm = ChatOpenAI(
    model=LLM_MODEL,
    openai_api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)

SYSTEM_PROMPT = """Eres un tutor experto en Spring Framework.
Ayudas a los desarrolladores a aprender Spring Boot, Spring Security,
Spring Data JPA y el ecosistema Spring en general.
Respondes siempre en español, de forma clara y con ejemplos de código cuando sea útil.

Cuando tengas contexto de la documentación, úsalo como base principal para responder.
Si el contexto no es suficiente, usa tu conocimiento general sobre Spring."""

def get_response(user_message: str) -> str:
    # 1. Busca contexto relevante en ChromaDB
    context = get_relevant_context(user_message)

    # 2. Construye el prompt con el contexto inyectado
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"""Contexto de la documentación:
{context}

Pregunta del usuario:
{user_message}""")
    ]

    # 3. LLM genera la respuesta con ese contexto
    response = llm.invoke(messages)
    return response.content