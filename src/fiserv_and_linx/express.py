import sys
import os
import time
import oathtool
import subprocess
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.Services.service_db import DataService

def get_server_option():
    """Captura a opção do terminal (1 ou 2)."""
    try:
        server = int(sys.argv[1])
        if server not in [1, 2]:
            raise ValueError
        return server
    except (IndexError, ValueError):
        print("Uso: python app.py <1=Elgin | 2=Connect>")
        sys.exit(1)

def timestamp():
    return str(datetime.now())[11:19]

def send_notification(message):
    """Envia notificação para o sistema."""
    subprocess.Popen(['notify-send', message])

def efetuar_login(server: int):
    """Realiza o login usando credenciais do banco."""
    service = DataService()
    
    try:
        # Busca credenciais no banco
        
        user, password, otp_key = service.get_credentials(server)
    except Exception as e:
        error_msg = f"[{timestamp()}] Erro: {str(e)}"
        send_notification(error_msg)
        print(error_msg)
        service.close()
        sys.exit(1)

    # Configuração do navegador
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print(f"[{timestamp()}] Iniciando login no servidor {'Elgin' if server == 1 else 'Connect'}")
        
        # Navegação e preenchimento do formulário
        driver.get("https://sitefexpressadm.softwareexpress.com.br/sitefwebadm/")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys(user)
        
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "username").submit()
        time.sleep(2)

        # Gera e preenche o OTP
        otp_code = oathtool.generate_otp(otp_key)
        for i in range(6):
            driver.find_element(By.ID, f"camp{i+1}").send_keys(otp_code[i])
        
        driver.find_element(By.XPATH, '//*[@id="kc-login"]').click()

        # Aguarda conclusão do login
        WebDriverWait(driver, 30).until(
            EC.url_to_be("https://sitefexpressadm.softwareexpress.com.br/sitefwebadm/pages/inicial.zeus")
        )
        print(f"[{timestamp()}] Login realizado com sucesso!")

    except Exception as e:
        error_msg = f"[{timestamp()}] Erro durante o login: {str(e)}"
        send_notification(error_msg)
        print(error_msg)
        driver.quit()
        service.close()
        sys.exit(1)

    return driver, service

def monitorar_janela(driver, service):
    """Monitora se a janela foi fechada."""
    try:
        while True:
            time.sleep(3)
            if not driver.title:
                break
    except Exception as e:
        send_notification(f"Erro: {str(e)}")
    finally:
        driver.quit()
        service.close()
        send_notification("Sessão encerrada")

if __name__ == "__main__":
    server = get_server_option()
    driver, service = efetuar_login(server)
    monitorar_janela(driver, service)