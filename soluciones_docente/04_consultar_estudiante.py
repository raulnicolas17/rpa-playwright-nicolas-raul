from playwright.sync_api import sync_playwright

PORTAL = "http://127.0.0.1:8000"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=250)
    page = browser.new_page()
    page.goto(PORTAL)

    for matricula in ("IAI0001", "IAI9999"):
        page.get_by_label("Matrícula").fill(matricula)
        page.get_by_role("button", name="Buscar").click()
        panel = page.get_by_test_id("result-panel")
        print(matricula, "->", " ".join(panel.inner_text().split()))

    browser.close()

