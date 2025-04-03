import os
import time
import oathtool  # type: ignore
import subprocess
from datetime import datetime
from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


path_main = f"{os.getcwd()}/"
this_file = "relatorio_express.py"


def timestamp():
    return str(datetime.now())[11:19]


def send_message(message):
    subprocess.Popen(['notify-send', message], )
    return


def get_cnpj():
    global id_cnpj

    reqMbR = open(f"{path_main}sysfiles/reqCnpj.txt", "r")
    id_cnpj = reqMbR.read()


def verify_path():
    global path_main
    combine = f"{path_main}{this_file}"
    print("#### ", combine)

    if os.path.exists(combine) is True:
        pass

    else:
        path_main = f"{path_main}TicketServer/"


def efetuar_login():
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
        send_message("Entrando em Relatório Express.")
        print(f"[INICIO]\n-- [{timestamp()}] Carregando credenciais")

        read_file = open(f"{path_main}sysfiles/auth.txt", "r").readlines()
        user = read_file[0].replace("\n", "")
        password = read_file[1].replace("\n", "")
        KEY = read_file[2].replace("\n", "")

    except Exception as e:
        print(f"[{timestamp()}] Erro ao obter credenciais!\n{e}")

    # Enter in Sitef Express to login
    try:
        print(f"-- [{timestamp()}] Efetuando login")

        driver.get(https_login)
        search_box_login = driver.find_element(By.NAME, 'username')
        search_box_login.send_keys(user)
        search_box_passw = driver.find_element(By.NAME, 'password')
        search_box_passw.send_keys(password)
        search_box_login.submit()
        time.sleep(2)

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
        driver.find_element(By.XPATH, '//*[@id="kc-login"]').click()

    except Exception as e:
        print(f"[{timestamp()}] Erro ao obter credenciais! \n{e}")

    # Waiting Access
    try:
        validar_janela = driver.current_url
        while validar_janela != https_home:
            time.sleep(1)
            validar_janela = driver.current_url

    except Exception as e:
        print(f"[{timestamp()}] Erro durante espera de acesso! \n{e}")


def acessar_relatorio():
    point = 0
    print(f"-- [{timestamp()}] Carregando Menu")

    while point == 0:
        try:
            # Simulate mouse on Menu Configurador
            menu_conf = driver.find_element(By.ID, "menuClientes")
            ActionChains(driver).move_to_element(menu_conf).perform()
            point_a = 0

            while point_a == 0:
                try:
                    # Click on Acessar in Menu Configurador
                    tag_acessar = menu_conf.find_elements(By.TAG_NAME, 'a')

                    for tag in tag_acessar:

                        try:
                            if tag.text == 'Listar Clientes':
                                tag.click()
                                point_a = 1

                        except Exception:
                            print(f"[{timestamp()}] Erro para encontrar o botão Listar Clientes!")

                except Exception:
                    print(f"[{timestamp()}] Erro ao clicar em Lista Clientes!")

            point = 1

        except Exception:
            print(f"[{timestamp()}] Erro ao acessar Lista de Clientes!")
            time.sleep(1)

    # Consultando Cliente
    point = 0

    while point == 0:
        try:
            print(f"-- [{timestamp()}] Consultando CNPJ")
            search_cnpj = driver.find_element(By.NAME, 'idTabelaClientes:j_idt309:filter')
            search_cnpj.send_keys(id_cnpj)
            search_cnpj.send_keys(Keys.ENTER)
            point = 1

        except Exception:
            print(f"[{timestamp()}] Erro ao Consulta CNPJ!")
            time.sleep(1)

    # Entrando no relatório
    point = 0

    while point == 0:
        try:
            print(f"-- [{timestamp()}] Entrando no relatório")
            search_cnpj = driver.find_element(By.ID, 'idTabelaClientes:0:j_idt339')
            search_cnpj.click()
            point = 1

        except Exception:
            print(f"[{timestamp()}] Erro clicar em relatório!")
            time.sleep(1)

    # Clicando no relatório
    point = 0

    while point == 0:
        try:
            print(f"-- [{timestamp()}] Clicando no relatório")
            search_cnpj = driver.find_element(By.ID, 'j_idt347:acessoexterno')
            search_cnpj.click()
            point = 1

        except Exception:
            print(f"[{timestamp()}] Erro clicar em relatório!")
            time.sleep(1)

    # Waiting Access
    print(f"-- [{timestamp()}] Fechando aba 0")

    # Change to tab 0 and close
    try:
        close_tab = driver
        close_tab.switch_to.window(driver.window_handles[0])
        close_tab.close()
    except Exception as e:
        send_message(f"Erro ao fechar aba 0! \n{e}")
        print(f"[{timestamp()}] Erro ao fechar aba 0! \n{e}")

    # Change to new tab 1 and continue
    driver.switch_to.window(driver.window_handles[0])   


def verify_close():
    try:
        while driver.title is not None:
            time.sleep(3)
    except Exception:
        send_message("Relatório Express fechado.")


if __name__ == "__main__":
    verify_path()
    get_cnpj()
    efetuar_login()
    acessar_relatorio()
    verify_close()
