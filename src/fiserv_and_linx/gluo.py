import sys
import subprocess
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def timestamp():
    return str(datetime.now())[11:19]

def send_notification(message):
    """Envia notificação para o sistema."""
    subprocess.Popen(['notify-send', message])

def monitorar_janela(driver):
    """Mantém a janela aberta até o usuário fechá-la."""
    print("🔴 Aguardando o fechamento da janela...")
    try:
        WebDriverWait(driver, timeout=10**6).until(lambda d: not d.window_handles)
    except KeyboardInterrupt:
        print("⛔ Interrupção manual detectada.")
    except Exception as e:
        print(f"⛔ Erro no monitoramento: {e}")

def acessar_tefway(username, password):
    """Acessa a página inicial da Tefway e realiza o login."""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        url = "https://tefway.app.gluocrm.com.br/index.php"
        print(f"[{timestamp()}] Acessando: {url}")

        driver.get(url)

        wait = WebDriverWait(driver, 20)

        # Preenche o campo de username
        username_field = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="inlineFormInputGroup username"]'))
        )
        username_field.send_keys(username)

        # Preenche o campo de password
        password_field = driver.find_element(By.XPATH, '//*[@id="inlineFormInputGroup password"]')
        password_field.send_keys(password)

        # Clica no botão de login
        login_button = driver.find_element(By.XPATH, '//*[@id="loginFormDiv"]/form/button')
        login_button.click()

        print(f"[{timestamp()}] Login efetuado. Mantendo a janela aberta...")

        monitorar_janela(driver)

    except Exception as e:
        error_msg = f"[{timestamp()}] Erro ao acessar a página: {str(e)}"
        print(error_msg)
        send_notification(error_msg)

    finally:
        driver.quit()
        print(f"[{timestamp()}] Navegador fechado.")

