from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PORTAL = "http://127.0.0.1:8000"
MATRICULA = "IAI0003"
EVIDENCIAS = ROOT / "evidencias"
DESCARGAS = ROOT / "descargas"
EVIDENCIAS.mkdir(exist_ok=True)
DESCARGAS.mkdir(exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=200)
    page = browser.new_page()
    try:
        page.goto(PORTAL)
        page.get_by_label("Matrícula").fill(MATRICULA)
        page.get_by_role("button", name="Buscar").click()
        panel = page.get_by_test_id("result-panel")
        panel.screenshot(path=EVIDENCIAS / f"resultado-{MATRICULA}.png")

        if "Matrícula inexistente" in panel.inner_text():
            print(f"Excepción de negocio: no existe {MATRICULA}")
        else:
            with page.expect_download() as download_info:
                page.get_by_role("button", name="Descargar kárdex").click()
            destino = DESCARGAS / f"kardex-{MATRICULA}.pdf"
            download_info.value.save_as(destino)
            print(f"Éxito: {MATRICULA} -> {destino}")
    except Exception as error:
        page.screenshot(path=EVIDENCIAS / f"error-tecnico-{MATRICULA}.png", full_page=True)
        print("Error técnico:", error)
    finally:
        browser.close()

