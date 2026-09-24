"""Reto: un agente clasifica y asigna un ticket conservando evidencia."""

import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PORTAL = "http://127.0.0.1:8010/login.html"
EVIDENCIAS = ROOT / "evidencias"
HEADLESS = os.getenv("CODESPACES") == "true"
EVIDENCIAS.mkdir(exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=HEADLESS, slow_mo=200)
    context = browser.new_context()
    page = context.new_page()

    try:
        page.goto(PORTAL)
        page.get_by_label("Usuario").fill("ana.agente")
        page.get_by_label("Contraseña").fill("soporte123")
        page.get_by_role("button", name="Iniciar sesión").click()
        page.get_by_role("heading", name="Panel de tickets").wait_for()

        rol = page.get_by_test_id("session-role")
        assert rol.inner_text() == "Agente"
        page.get_by_role("button", name="Abrir INC-1001").click()
        detalle = page.get_by_test_id("ticket-detail")
        detalle.wait_for()

        page.get_by_label("Prioridad", exact=True).select_option(label="Alta")
        page.get_by_label("Grupo asignado", exact=True).select_option(label="Seguridad")
        page.get_by_label("Estado", exact=True).select_option(label="En proceso")

        page.get_by_role("button", name="Guardar cambios").click()
        confirmacion = page.get_by_role("status")
        confirmacion.wait_for()
        assert confirmacion.inner_text() == "Cambios guardados para INC-1001."

        assert page.locator("#detail-priority").inner_text() == "Alta"
        assert page.locator("#detail-group").inner_text() == "Seguridad"
        assert page.locator("#detail-status").inner_text() == "En proceso"

        evidencia = EVIDENCIAS / "INC-1001-actualizado.png"
        detalle.screenshot(path=evidencia)

        print("Ticket: INC-1001")
        print("Prioridad: Alta")
        print("Grupo: Seguridad")
        print("Estado: En proceso")
        print("Evidencia:", evidencia)
    except Exception as error:
        page.screenshot(path=EVIDENCIAS / "error-tecnico.png", full_page=True)
        print("Error técnico:", error)
        raise
    finally:
        browser.close()
