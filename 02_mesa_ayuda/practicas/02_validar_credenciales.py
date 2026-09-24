"""Práctica 2: diferencia un resultado esperado de un error técnico."""

import os
from playwright.sync_api import sync_playwright

PORTAL = "http://127.0.0.1:8010/login.html"
HEADLESS = os.getenv("CODESPACES") == "true"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=HEADLESS)
    page = browser.new_page()
    page.goto(PORTAL)

    page.get_by_label("Usuario").fill("maria.solicitante")
    page.get_by_label("Contraseña").fill("incorrecta")
    page.get_by_role("button", name="Iniciar sesión").click()

    alerta = page.get_by_role("alert")
    alerta.wait_for()
    print("Mensaje:", alerta.inner_text())

    assert page.url.endswith("login.html"), "La URL cambió inesperadamente."
    print("Continúa en login:", page.url)

    browser.close()
