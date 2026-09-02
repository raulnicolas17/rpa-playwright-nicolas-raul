"""Reto: consulta, valida, descarga y conserva evidencia."""

from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PORTAL = "http://127.0.0.1:8000"

# Cambie esta entrada para probar el camino feliz o una excepción de negocio.
MATRICULAS = ["IAI0003", "IAI9999"]
EVIDENCIAS = ROOT / "evidencias"
DESCARGAS = ROOT / "descargas"
EVIDENCIAS.mkdir(exist_ok=True)
DESCARGAS.mkdir(exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=200)
    page = browser.new_page()

    try:
        page.goto(PORTAL)
        for MATRICULA in MATRICULAS:
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
        # TODO 2: capturar MATRICULA y buscar.
        # Utilice localizadores semánticos por etiqueta, rol y nombre.
        
        # TODO 3: decidir si es éxito o excepción de negocio.
        # Lea el texto del panel. Una matrícula inexistente no es necesariamente
        # un error técnico: es un resultado previsto por las reglas del proceso.

        # TODO 4: si es éxito, descargar el kárdex.
        # Prepare expect_download() antes del clic y controle la ruta final.

        # TODO 5: guardar una captura con la matrícula en el nombre.
        # Incluir el identificador del caso facilita relacionar la evidencia.

        # TODO 6: imprimir un resultado comprensible.
        # La salida debería distinguir éxito, excepción de negocio y fallo.
        pass

    # Esta captura genérica simplifica el laboratorio. En un sistema real se
    # utilizarían excepciones más específicas y logs estructurados.
