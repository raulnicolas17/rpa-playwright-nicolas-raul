"""Comprobación técnica: abre el portal de mesa de ayuda y valida el formulario."""

import os
from playwright.sync_api import sync_playwright

PORTAL = "http://127.0.0.1:8010/login.html"
HEADLESS = os.getenv("CODESPACES") == "true"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=HEADLESS)
    page = browser.new_page()
    page.goto(PORTAL)

    heading = page.get_by_role("heading", name="Iniciar sesión")
    print("Título:", page.title())
    print("Formulario visible:", heading.is_visible())

    assert heading.is_visible(), "No se encontró el formulario de acceso."
    browser.close()

print("Entorno listo.")
