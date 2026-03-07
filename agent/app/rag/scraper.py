import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document
import time

# URLs de la documentación oficial de Spring a scrapear
SPRING_DOCS_URLS = [
    # Spring Boot
    "https://docs.spring.io/spring-boot/docs/current/reference/html/getting-started.html",
    "https://docs.spring.io/spring-boot/docs/current/reference/html/using.html",
    "https://docs.spring.io/spring-boot/docs/current/reference/html/application-properties.html",
    # Spring Data JPA
    "https://docs.spring.io/spring-data/jpa/docs/current/reference/html/",
]

def scrape_page(url: str) -> Document | None:
    """
    Descarga una página de la documentación y extrae el texto limpio.
    Devuelve un Document de LangChain con el contenido y la URL como metadata.
    """
    try:
        print(f"🌐 Scrapeando: {url}")
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"⚠️  Error {response.status_code} en {url}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Elimina scripts, estilos y navegación para quedarnos solo con el contenido
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # Extrae el texto limpio
        text = soup.get_text(separator="\n", strip=True)

        # Elimina líneas vacías consecutivas
        lines = [line for line in text.splitlines() if line.strip()]
        clean_text = "\n".join(lines)

        return Document(
            page_content=clean_text,
            metadata={"source": url, "type": "web"}
        )

    except Exception as e:
        print(f"❌ Error scrapeando {url}: {e}")
        return None


def scrape_spring_docs() -> list[Document]:
    """
    Scrapea todas las URLs definidas y devuelve la lista de documentos.
    """
    documents = []

    for url in SPRING_DOCS_URLS:
        doc = scrape_page(url)
        if doc:
            documents.append(doc)
        # Pausa entre peticiones para no saturar el servidor
        time.sleep(1)

    print(f"✅ {len(documents)} páginas scrapeadas correctamente")
    return documents