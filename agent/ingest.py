from app.rag.loader import load_and_split
from app.rag.scraper import scrape_spring_docs
from app.rag.vectorstore import build_vectorstore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP

def main():
    print("🚀 Iniciando ingesta de documentación...")

    # 1. Carga archivos .md locales
    local_chunks = load_and_split()

    # 2. Scrapea documentación oficial
    print("\n📡 Iniciando web scraping...")
    web_documents = scrape_spring_docs()

    # 3. Trocea los documentos web igual que los locales
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    web_chunks = splitter.split_documents(web_documents)
    print(f"✂️  {len(web_chunks)} chunks generados del scraping")

    # 4. Combina todos los chunks
    all_chunks = local_chunks + web_chunks
    print(f"\n📦 Total chunks a indexar: {len(all_chunks)}")

    # 5. Guarda todo en ChromaDB
    build_vectorstore(all_chunks)

    print("🎉 Ingesta completada. ChromaDB listo para buscar.")

if __name__ == "__main__":
    main()