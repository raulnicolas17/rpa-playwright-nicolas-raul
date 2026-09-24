"""Práctica 3: guarda cookies y almacenamiento local de una sesión autenticada."""

import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PORTAL = "http://127.0.0.1:8010/login.html"
ESTADO = ROOT / ".auth" / "solicitante.json"
HEADLESS = os.getenv("CODESPACES") == "true"
ESTADO.parent.mkdir(exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=HEADLESS)
    context = browser.new_context()
    page = context.new_page()
    page.goto(PORTAL)

    page.get_by_label("Usuario").fill("maria.solicitante")
    page.get_by_label("Contraseña").fill("rpa123")
    page.get_by_role("button", name="Iniciar sesión").click()
    page.get_by_role("heading", name="Panel de tickets").wait_for()

    context.storage_state(path=ESTADO)
    browser.close()

assert ESTADO.exists(), "No se creó el archivo de estado."
print("Estado guardado en:", ESTADO)
print("Tamaño:", ESTADO.stat().st_size, "bytes")
