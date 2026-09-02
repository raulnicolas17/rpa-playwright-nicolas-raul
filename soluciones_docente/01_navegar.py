from playwright.sync_api import sync_playwright

PORTAL = "http://127.0.0.1:8000"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page()
    page.goto(PORTAL)
    print("Título:", page.title())
    print("URL:", page.url)
    browser.close()

