from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PORTAL = "http://127.0.0.1:8000"
EVIDENCIAS = ROOT / "evidencias"
EVIDENCIAS.mkdir(exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(PORTAL)
    page.screenshot(path=EVIDENCIAS / "portal.png", full_page=True)
    page.get_by_role("heading", name="Consulta de kárdex").screenshot(
        path=EVIDENCIAS / "encabezado.png"
    )
    browser.close()

print("Evidencias guardadas en:", EVIDENCIAS)

