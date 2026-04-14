import json
from playwright.sync_api import sync_playwright

url = "https://www.gatesnotes.com/books/all-book-reviews"

def run():
    with sync_playwright() as p:
        # Modo headed=False abre la ventana. Interesantemente, Cloudflare suele
        # bloquear menos un navegador que tiene cabeza visible.
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print("Navegando a GatesNotes...")
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        all_books = []
        seen = set() # Evita duplicados
        last_height = page.evaluate("document.body.scrollHeight")

        print("Extrayendo datos dinámicamente durante el desplazamiento...")
        for i in range(25):
            # Extraemos los artículos que existen AHORA MISMO en el DOM
            items = page.locator(".ArticleListItem").all()
            for item in items:
                title_el = item.locator(".CampaignArticlesTitle")
                if title_el.count() > 0:
                    title = title_el.inner_text().strip()
                    url_href = title_el.get_attribute("href")

                    author_el = item.locator(".CampaignArticlesName")
                    author = author_el.inner_text().strip() if author_el.count() > 0 else ""

                    cat_el = item.locator(".KBreadCrumbCopy")
                    cat = cat_el.inner_text().strip() if cat_el.count() > 0 else ""

                    if url_href not in seen:
                        seen.add(url_href)
                        all_books.append({
                            "title": title, "author": author, "category": cat, "url": url_href
                        })

            print(f"Iteración {i+1}: Van {len(all_books)} libros únicos extraídos.")

            # Simulamos la tecla "Avance de Página" para activar la carga diferida
            for _ in range(3):
                page.keyboard.press("PageDown")
                page.wait_for_timeout(500)

            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height and i > 5:
                # Comprobamos si tocamos el final exacto
                page.keyboard.press("End")
                page.wait_for_timeout(1500)
                if page.evaluate("document.body.scrollHeight") == last_height:
                    print("Llegamos al final del contenido.")
                    break
            last_height = new_height

        print(f"¡Extracción finalizada! Libros extraídos en total: {len(all_books)}")

        # Guardamos a formato JSON estructurado
        with open("gatesnotes_books.json", "w", encoding="utf-8") as f:
            json.dump(all_books, f, indent=4, ensure_ascii=False)
        print("Datos guardados en gatesnotes_books.json")

        browser.close()

if __name__ == "__main__":
    run()
