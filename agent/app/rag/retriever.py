from app.rag.vectorstore import get_vectorstore
from app.config import TOP_K_RESULTS

def get_relevant_context(question: str) -> str:
    """
    Dado un mensaje del usuario, busca en ChromaDB los chunks
    más relevantes y los devuelve como un solo texto de contexto.
    """
    vectorstore = get_vectorstore()

    # Busca los TOP_K_RESULTS chunks más similares a la pregunta
    relevant_chunks = vectorstore.similarity_search(
        query=question,
        k=TOP_K_RESULTS
    )

    if not relevant_chunks:
        return "No se encontró documentación relevante."

    # Une todos los chunks en un solo texto separado por líneas
    context = "\n\n---\n\n".join([chunk.page_content for chunk in relevant_chunks])

    print(f"🔍 {len(relevant_chunks)} chunks relevantes encontrados")
    return context