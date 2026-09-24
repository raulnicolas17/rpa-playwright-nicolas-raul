"""Práctica 4: abre el área protegida sin repetir el formulario de acceso."""

import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = "http://127.0.0.1:8010/dashboard.html"
ESTADO = ROOT / ".auth" / "solicitante.json"
HEADLESS = os.getenv("CODESPACES") == "true"

if not ESTADO.exists():
    raise FileNotFoundError("Ejecute primero 03_guardar_sesion.py")

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=HEADLESS)
    context = browser.new_context(storage_state=ESTADO)
    page = context.new_page()
    page.goto(DASHBOARD)

    rol = page.get_by_test_id("session-role")
    assert rol.inner_text() == "Solicitante"
    print("Perfil restaurado:", rol.inner_text())

    tickets = page.locator("[data-ticket-id]").count()
    print("Tickets visibles:", tickets)
    assert tickets == 2

    page.get_by_role("button", name="Cerrar sesión").click()
    page.wait_for_url("**/login.html")
    assert page.url.endswith("login.html")
    print("Sesión cerrada correctamente.")

    browser.close()
