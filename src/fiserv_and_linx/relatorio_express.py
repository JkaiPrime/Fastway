import os
import sys
import time
import oathtool  # type: ignore
import subprocess
from datetime import datetime
from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.Services.service_db import DataService
service = DataService()

global cnpj
global server

def timestamp():
    return str(datetime.now())[11:19]


def waiting_element(driver, element_type, element, timeout=30):
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((element_type, element))
    )


def format_cnpj(varcnpj='', mask=True):
    '''This function verify if CNPJ has mask and converto to standard (with
    mask) or not (without mask).'''

    string_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    varcnpj = varcnpj.strip()

    if mask is True:
        # Remove any character that is not a number
        for i in varcnpj:
            if i not in string_numbers:
                varcnpj = varcnpj.replace(i, "")

        # Put mask
        varcnpj_1 = varcnpj[:2] + '.' + varcnpj[2:5] + '.' + varcnpj[5:8]
        varcnpj_2 = '/' + varcnpj[8:12] + '-' + varcnpj[12:14]
        varcnpj = varcnpj_1 + varcnpj_2

    else:
        # Remove any character that is not a number
        for i in varcnpj:
            if i not in string_numbers:
                varcnpj = varcnpj.replace(i, "")

    return varcnpj


def try_click(brws: WebDriver, path='', tries=5):
    """O path funciona apenas com o XPATH."""
    # for i in range(tries):
    i = 0
    while i < tries:
        try:
            brws.find_element(By.XPATH, path).click()
            # brws.switch_to.alert.accept()
            break
        except Exception:
            time.sleep(3)
            i += 1
            continue


def efetuar_login(server:int):
    global driver


    https_express = "https://sitefexpressadm.softwareexpress.com.br/"
    https_home = f"{https_express}sitefwebadm/pages/inicial.zeus"
    https_login = f"{https_express}sitefwebadm/"

    # Config ChromeDriver
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    # Get credentials
    try:
        user,password,KEY = service.get_credentials(server)


    except Exception as e:
        sys.exit()

    # Enter in Sitef Express to login
    max_login_tries = 3

    while True:


        driver.get(https_login)
        search_box_login = driver.find_element(By.NAME, 'username')
        search_box_login.send_keys(user)
        search_box_passw = driver.find_element(By.NAME, 'password')
        search_box_passw.send_keys(password)
        search_box_login.submit()

        var = oathtool.generate_otp(KEY)

        var_u = var[0]
        var_d = var[1]
        var_t = var[2]
        var_q = var[3]
        var_c = var[4]
        var_s = var[5]

        click_primeiro_campo = driver.find_element(By.ID, 'camp1')
        click_primeiro_campo.send_keys(f'''{var_u}''')
        click_segundo_campo = driver.find_element(By.ID, 'camp2')
        click_segundo_campo.send_keys(f'''{var_d}''')
        click_terceiro_campo = driver.find_element(By.ID, 'camp3')
        click_terceiro_campo.send_keys(f'''{var_t}''')
        click_quarto_campo = driver.find_element(By.ID, 'camp4')
        click_quarto_campo.send_keys(f'''{var_q}''')
        click_quinto_campo = driver.find_element(By.ID, 'camp5')
        click_quinto_campo.send_keys(f'''{var_c}''')
        click_sexto_campo = driver.find_element(By.ID, 'camp6')
        click_sexto_campo.send_keys(f'''{var_s}''')
        try_click(driver, path='//*[@id="kc-login"]', tries=5)

        # Valida se deu erro
        try:
            time.sleep(2)
            driver.find_element(By.ID, "feedbackCodigoInvalido")

            max_login_tries -= 1
            print("tentativa: ", max_login_tries)

            if max_login_tries == 0:
                sys.exit()

        except Exception:
            break

    # Waiting Access
    try:
        validar_janela = driver.current_url
        while validar_janela != https_home:
            time.sleep(1)
            validar_janela = driver.current_url

    except Exception as e:
        sys.exit()


def acessar_relatorio(cnpj:str):
    menu_acesso = driver.find_element(By.XPATH, "//a[contains(text(), 'Listar Clientes')]")
    script = menu_acesso.get_attribute("onclick")
    driver.execute_script(script)

    # Insere o CNPJ e pesquisa (menu principal ainda)
    waiting_element(driver, By.XPATH, '//*[@id="idTabelaClientes_head"]/tr/th[3]/input')
    driver.find_element(By.XPATH, '//*[@id="idTabelaClientes_head"]/tr/th[3]/input').send_keys(cnpj)
    driver.find_element(By.XPATH, '//*[@id="idTabelaClientes_head"]/tr/th[3]/input').send_keys(Keys.ENTER)

    # Valida se só existe ele e entra nele
    while True:
        if driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/form/div[1]/fieldset/div/div[2]/span[1]').text == '1 de 1 (1 de 1 registros)':
            menu_acesso = driver.find_element(By.XPATH, "//a[@title='Acessar Interface de Relatórios']")
            script = menu_acesso.get_attribute("onclick")
            driver.execute_script(script)

            break

        if driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/form/div[1]/fieldset/div/div[2]/span[1]').text == '1 de 1 (0 de 0 registros)':

            sys.exit()

    # Clicando no "Acessar" para abrir a aba de relatório
    waiting_element(driver, By.XPATH, "//a[@class='tryitbtn botaoAcessoRel']")
    driver.find_element(By.XPATH, "//a[@class='tryitbtn botaoAcessoRel']").click()

    # Waiting Access and close tab 0
    try:
        close_tab = driver
        close_tab.switch_to.window(driver.window_handles[0])
        close_tab.close()

    except Exception as e:

        sys.exit()

    # Change to new tab 1 and continue
    driver.switch_to.window(driver.window_handles[0])


def verify_close():
    try:
        while True:
            if len(driver.window_handles) == 0:
                break
            time.sleep(3)
    except Exception as e:
        print(f"Erro: {str(e)}")
    finally:
        driver.quit()
        service.close()
        

def run(server_desc:str, cnpj_client:str):
    server = server_desc
    cnpj = cnpj_client
    efetuar_login(server)
    acessar_relatorio(cnpj)
    verify_close()


