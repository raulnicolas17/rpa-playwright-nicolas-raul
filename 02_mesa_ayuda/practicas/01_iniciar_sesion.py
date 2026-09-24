"""Práctica 1: automatiza un inicio de sesión correcto e identifica el perfil."""

import os
from playwright.sync_api import sync_playwright

PORTAL = "http://127.0.0.1:8010/login.html"
HEADLESS = os.getenv("CODESPACES") == "true"
USUARIO = "maria.solicitante"
CONTRASENA = "rpa123"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=HEADLESS, slow_mo=250)
    page = browser.new_page()
    page.goto(PORTAL)

    page.get_by_label("Usuario").fill(USUARIO)
    page.get_by_label("Contraseña").fill(CONTRASENA)
    page.get_by_role("button", name="Iniciar sesión").click()
    page.get_by_role("heading", name="Panel de tickets").wait_for()

    rol = page.get_by_test_id("session-role").inner_text()
    print("Perfil autenticado:", rol)

    browser.close()
