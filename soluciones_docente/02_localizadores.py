from playwright.sync_api import sync_playwright

PORTAL = "http://127.0.0.1:8000"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(PORTAL)
    encabezado = page.get_by_role("heading", name="Consulta de kárdex")
    campo = page.get_by_label("Matrícula")
    boton = page.get_by_role("button", name="Buscar")
    print("Encabezado:", encabezado.text_content())
    print("Campo visible:", campo.is_visible())
    print("Botón visible:", boton.is_visible())
    browser.close()

