import os
from dotenv import load_dotenv

load_dotenv()

# ===========================
# LLM
# ===========================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")

# ===========================
# RAG
# ===========================

# Carpeta donde están los archivos .md con documentación
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Carpeta donde ChromaDB guardará los vectores
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

# Nombre de la colección dentro de ChromaDB
CHROMA_COLLECTION = "spring_docs"

# Número de chunks relevantes que se recuperan por pregunta
TOP_K_RESULTS = 8

# Tamaño de cada chunk en caracteres
CHUNK_SIZE = 1000

# Solapamiento entre chunks (para no perder contexto en los cortes)
CHUNK_OVERLAP = 200