import os
import time
import oathtool  # type: ignore
import subprocess
from datetime import datetime
from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.action_chains import ActionChains


def verify_path():
    global path_main

    path_main = f"{os.getcwd()}/"
    this_file = "relatorio_express.py"
    combine = f"{path_main}{this_file}"
    print("#### ", combine)

    if os.path.exists(combine) is True:
        pass

    else:
        path_main = f"{path_main}TicketServer/"


def timestamp():
    return str(datetime.now())[11:19]


def send_message(message):
    subprocess.Popen(['notify-send', message], )
    return


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
        print(f"[INICIO]\n-- [{timestamp()}] Carregando credenciais")

        read_file = open(f"{path_main}sysfiles/auth.txt", "r").readlines()
        user = read_file[0].replace("\n", "")
        password = read_file[1].replace("\n", "")
        KEY = read_file[2].replace("\n", "")

    except Exception as e:
        message = f"[{timestamp()}] Erro ao obter credenciais!\n{e}"
        send_message(message)
        print(message)

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
        message = f"[{timestamp()}] Erro ao obter credenciais! \n{e}"
        send_message(message)
        print(message)

    # Waiting Access
    try:
        validar_janela = driver.current_url
        while validar_janela != https_home:
            time.sleep(1)
            validar_janela = driver.current_url

    except Exception as e:
        message = f"[{timestamp()}] Erro durante espera de acesso! \n{e}"
        send_message(message)
        print(message)


def acessar_configurador():
    point = 0
    print(f"-- [{timestamp()}] Carregando Menu")

    while point == 0:
        try:
            # Simulate mouse on Menu Configurador
            menu_conf = driver.find_element(By.ID, "menuConfigurador")
            ActionChains(driver).move_to_element(menu_conf).perform()
            point_a = 0

            while point_a == 0:
                try:
                    # Click on Acessar in Menu Configurador
                    tag_acessar = menu_conf.find_elements(By.TAG_NAME, 'a')

                    for tag in tag_acessar:

                        try:
                            if tag.text == 'Acessar':
                                tag.click()
                                point_a = 1

                        except Exception as e:
                            message_1 = f"[{timestamp()}] Erro para encontrar"
                            message = f"{message_1} o botão Acessar! \n{e}"
                            send_message(message)
                            print(message)

                except Exception:
                    message_1 = f"[{timestamp()}] Erro ao clicar em"
                    message = f"{message_1} Acessar configurador!"
                    send_message(message)
                    print(message)

            point = 1

        except Exception:
            message = f"[{timestamp()}] Erro ao acessar configurador!"
            send_message(message)
            print(message)
            time.sleep(1)

    # Waiting Access
    try:
        print(f"-- [{timestamp()}] Acessando configurador")

        # Change to tab 0 and close
        try:
            close_tab = driver
            close_tab.switch_to.window(driver.window_handles[0])
            close_tab.close()
        except Exception as e:
            message = f"[{timestamp()}] Erro ao fechar aba 0! \n{e}"
            send_message(message)
            print(message)

        # Change to new tab 1 and continue
        driver.switch_to.window(driver.window_handles[0])
        validar_janela = driver.title

        while validar_janela != "Menu SiTef":
            time.sleep(1)
            validar_janela = driver.current_url

        if validar_janela == "Menu SiTef":
            message = f"-- [{timestamp()}] Configurador acessado com sucesso!"
            send_message(message)
            print(message)

    except Exception as e:
        message = f"[{timestamp()}] Erro durante espera de acesso! \n{e}"
        send_message(message)
        print(message)


def verify_close():
    try:
        while driver.title is not None:
            time.sleep(3)
    except Exception:
        send_message("Configurador Express fechado.")

    # try:
    #     count = 0
    #     while count == 0:
    #         if driver.title is True:
    #             time.sleep(3)
    #         else:
    #             send_message("Entrou no Else")
    #             time.sleep(10)
    #             if driver.title is False:
    #                 count = 1

    except Exception:
        send_message("Configurador Express fechado.")


if __name__ == "__main__":
    verify_path()
    efetuar_login()
    acessar_configurador()
    verify_close()
