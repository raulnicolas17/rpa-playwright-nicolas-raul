from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PORTAL = "http://127.0.0.1:8000"
MATRICULA = "IAI0002"
DESCARGAS = ROOT / "descargas"
DESCARGAS.mkdir(exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=250)
    page = browser.new_page()
    page.goto(PORTAL)
    page.get_by_label("Matrícula").fill(MATRICULA)
    page.get_by_role("button", name="Buscar").click()

    with page.expect_download() as download_info:
        page.get_by_role("button", name="Descargar kárdex").click()
    download = download_info.value
    destino = DESCARGAS / f"kardex-{MATRICULA}.pdf"
    download.save_as(destino)
    print("Descarga guardada en:", destino)
    browser.close()

