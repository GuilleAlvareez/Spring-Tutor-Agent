from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP

def load_documents():
    """
    Lee todos los archivos .md de la carpeta data/
    y los devuelve como lista de documentos LangChain
    """
    loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.md",        # busca todos los .md recursivamente
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    documents = loader.load()
    print(f"📄 {len(documents)} archivos cargados desde {DATA_DIR}")
    return documents


def split_documents(documents):
    """
    Trocea los documentos en chunks más pequeños
    para que el LLM pueda procesarlos mejor
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,       # tamaño máximo de cada chunk
        chunk_overlap=CHUNK_OVERLAP, # solapamiento para no perder contexto
    )

    chunks = splitter.split_documents(documents)
    print(f"✂️  {len(chunks)} chunks generados")
    return chunks


def load_and_split():
    """
    Función principal: carga y trocea en un solo paso
    """
    documents = load_documents()
    return split_documents(documents)