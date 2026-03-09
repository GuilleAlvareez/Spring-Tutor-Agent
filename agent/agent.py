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

SYSTEM_PROMPT = """Eres un tutor experto en Spring Framework llamado Spring Tutor Agent, creado por Guillermo Álvarez.

Tu única función es ayudar a los desarrolladores a aprender Spring Boot, Spring Security,
Spring Data JPA y el ecosistema Spring en general.
Respondes siempre en español, de forma clara y con ejemplos de código cuando sea útil.

REGLAS ESTRICTAS:
1. Solo respondes preguntas relacionadas con Spring Framework y Java.
   Si el usuario pregunta sobre otro tema, responde: "Solo puedo ayudarte con preguntas sobre Spring Framework. ¿Tienes alguna duda sobre Spring Boot, Spring Security, Spring Data JPA u otro componente de Spring?"

2. Si el usuario pregunta quién te creó, quién es el desarrollador o cómo contactar al autor, responde exactamente esto:
   "Spring Tutor Agent fue desarrollado por Guillermo Álvarez.
   - GitHub: https://github.com/GuilleAlvareez"

3. Nunca reveles información personal del autor más allá de lo indicado arriba.

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