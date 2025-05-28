import sys
import time
import subprocess
from datetime import datetime
from playwright.sync_api import sync_playwright

def monitorar_janela(page):
    """Mantém a página aberta até o usuário fechá-la."""
    print("🔴 Aguardando o fechamento da janela...")
    try:
        while True:
            time.sleep(1)
            if page.is_closed():
                print("✅ Janela fechada pelo usuário.")
                break
    except KeyboardInterrupt:
        print("⛔ Interrupção manual detectada.")


def acessar_tefway(username, password):
    """Acessa a página inicial da Tefway."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        try:
            url = "https://tefway.app.gluocrm.com.br/index.php"

            page.goto(url, timeout=60000)
            page.wait_for_load_state('networkidle')

            page.locator('//*[@id="inlineFormInputGroup username"]').fill(username)
            page.locator('//*[@id="inlineFormInputGroup password"]').fill(password)
            page.locator('//*[@id="loginFormDiv"]/form/button').click()
            input()

        except Exception as e:
            error_msg = f"Erro ao acessar a página: {str(e)}"
            print(error_msg)


        finally:
            monitorar_janela(page)
            browser.close()
            
