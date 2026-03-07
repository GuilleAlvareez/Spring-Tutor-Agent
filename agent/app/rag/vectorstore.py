from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from app.config import (
    OPENROUTER_API_KEY,
    CHROMA_DIR,
    CHROMA_COLLECTION,
)

def get_embeddings():
    """
    Los embeddings convierten texto en vectores numéricos.
    Usamos el modelo de embeddings de OpenAI compatible con OpenRouter.
    """
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )


def get_vectorstore():
    """
    Devuelve la instancia de ChromaDB existente.
    Se usa para buscar chunks cuando el usuario pregunta algo.
    """
    return Chroma(
        collection_name=CHROMA_COLLECTION,
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_DIR,
    )


def build_vectorstore(chunks):
    """
    Crea ChromaDB desde cero con los chunks proporcionados.
    Se ejecuta solo una vez al indexar la documentación.
    """
    print("🔨 Construyendo vectorstore...")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        collection_name=CHROMA_COLLECTION,
        persist_directory=CHROMA_DIR,
    )

    print(f"✅ Vectorstore creado con {len(chunks)} chunks")
    return vectorstore