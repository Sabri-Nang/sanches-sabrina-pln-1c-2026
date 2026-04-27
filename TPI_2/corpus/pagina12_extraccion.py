import json
from playwright.sync_api import sync_playwright

data = []

urls =  ["https://www.pagina12.com.ar/2026/02/13/todos-los-derechos-con-los-que-arrasa-la-reforma-laboral-de-milei/",
         "https://www.pagina12.com.ar/2026/03/06/milei-promulgo-su-reforma-laboral-uno-por-uno-todos-los-derechos-que-pierden-los-trabajadores/",
         "https://www.pagina12.com.ar/2026/02/21/el-futuro-del-trabajo-con-la-reforma-laboral/",
         "https://www.pagina12.com.ar/2026/03/06/el-impacto-de-la-reforma-laboral/"]


for url in urls:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)


        # Minimizamos avisos de pantalla
        try:
            boton = page.wait_for_selector('button:has-text("Aceptar")', timeout=3000)
            if boton: boton.click()
        except:
            pass

        # Esperamos que cargue la portada
        print("Esperando confirmación del renderizado...")
        page.wait_for_selector("article", timeout=10000)
        page.wait_for_timeout(2000)  # Damos tiempo extra para carga diferida


        #print("Recolectando artículos con contexto seccional...")

        data_noticia = page.evaluate("""
        () => {
            // 1. Título
            const titulo = document.querySelector('h1')?.innerText.trim() || 
                        document.querySelector('.article-title')?.innerText.trim();

            // 2. Autor
            // Página12 suele usar .article-author o clases similares
            const autor = document.querySelector('.article-author')?.innerText.trim() || 
                        document.querySelector('.author-name')?.innerText.trim() || 
                        "Autor no encontrado";

            // 3. Fecha
            // Buscamos en el atributo 'datetime' de la etiqueta <time> si existe
            const fechaEl = document.querySelector('time');
            const fecha = fechaEl ? (fechaEl.getAttribute('datetime') || fechaEl.innerText.trim()) : "Fecha no encontrada";

            // 4. Medio
            const medio = "Página|12";

            // 5. Texto (Cuerpo de la noticia)
            // Seleccionamos solo los párrafos dentro del contenedor de la noticia
            // para evitar el ruido del menú lateral y banners
            const contenedorTexto = document.querySelector('.article-main-content') || 
                                    document.querySelector('.article-text') || 
                                    document.querySelector('article');

            let texto = "";
            if (contenedorTexto) {
                const parrafos = contenedorTexto.querySelectorAll('p');
                // Filtramos párrafos vacíos o muy cortos que suelen ser publicidad
                texto = Array.from(parrafos)
                            .map(p => p.innerText.trim())
                            .filter(t => t.length > 20)
                            .join('\\n\\n');
            }

            return {
                titulo: titulo,
                autor: autor,
                fecha: fecha,
                medio: medio,
                texto: texto
            };
        }
        """)

        print("--- RESULTADO DE LA EXTRACCIÓN ---")
        print(json.dumps(data_noticia, indent=4, ensure_ascii=False))

        browser.close()
        data.append(data_noticia)



# Guardamos el corpus
with open("pagina12.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Archivo 'pagina12.json' guardado correctamente.")

