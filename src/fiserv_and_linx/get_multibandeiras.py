import os
import time
import oathtool  # type: ignore
import openpyxl
import subprocess  # para notificar no Linux
import pandas as pd
from datetime import datetime
from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


path_main = f"{os.getcwd()}/"
this_file = "get_multibandeiras.py"


def send_message(message):
    subprocess.Popen(['notify-send', message], )
    return


def get_idsitef():
    global id_sitef

    reqMbR = open(f"{path_main}sysfiles/reqMb.txt", "r")
    id_sitef = reqMbR.read()


def verify_path():
    global path_main
    combine = f"{path_main}{this_file}"
    print("#### ", combine)

    if os.path.exists(combine) is True:
        pass

    else:
        path_main = f"{path_main}TicketServer/"


def get_url_modulo(modulo):
    '''This function is to return url to right
    Módulo from Visualizador de Tabelas.
    '''
    global url_visual_modulo

    url_modulo = {
        "cardse": "C1D548606BBD9299BE3A0E5D2AAF97D154EDE76630D3E36E443975AAB9A8F18499E76711E93B9F74"
    }

    for i in url_modulo:
        if modulo == i:
            url_visual_modulo = url_modulo[i]


def timestamp():
    return str(datetime.now())[11:19]


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
        send_message("Obtendo multibandeiras!")
        print(f"[INICIO]\n-- [{timestamp()}] Carregando credenciais")

        read_file = open(f"{path_main}sysfiles/auth.txt", "r").readlines()
        user = read_file[0].replace("\n", "")
        password = read_file[1].replace("\n", "")
        KEY = read_file[2].replace("\n", "")

    except Exception as e:
        send_message(f"Erro ao obter credenciais! \n{e}")
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
        send_message(f"Erro ao obter credenciais! \n{e}")
        print(f"[{timestamp()}] Erro ao obter credenciais! \n{e}")

    # Waiting Access
    try:
        validar_janela = driver.current_url
        while validar_janela != https_home:
            time.sleep(1)
            validar_janela = driver.current_url

    except Exception as e:
        send_message(f"Erro durante espera de acesso! \n{e}")
        print(f"[{timestamp()}] Erro durante espera de acesso! \n{e}")


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
                            send_message(f"Erro para encontrar o botão Acessar! \n{e}")
                            print(f"[{timestamp()}] Erro para encontrar o botão Acessar! \n{e}")

                except Exception:
                    send_message(f"Erro ao clicar em Acessar configurador! \n{e}")
                    print(f"[{timestamp()}] Erro ao clicar em Acessar configurador!")

            point = 1

        except Exception:
            send_message(f"Erro ao acessar configurador! \n{e}")
            print(f"[{timestamp()}] Erro ao acessar configurador!")
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
            send_message(f"Erro ao fechar aba 0! \n{e}")
            print(f"[{timestamp()}] Erro ao fechar aba 0! \n{e}")

        # Change to new tab 1 and continue
        driver.switch_to.window(driver.window_handles[0])
        validar_janela = driver.title

        while validar_janela != "Menu SiTef":
            time.sleep(1)
            validar_janela = driver.current_url

        if validar_janela == "Menu SiTef":
            print(f"-- [{timestamp()}] Configurador acessado com sucesso!")

    except Exception as e:
        print(f"[{timestamp()}] Erro durante espera de acesso! \n{e}")


def consultar_multibandeiras(id_sitef):
    # Open new tab as Multibandeiras
    print(f"-- [{timestamp()}] Entrando em Multibandeiras")

    url_main = "https://sitefexpressadmsc.softwareexpress.com.br"
    url_multib = f"{url_main}/elgin/multibandeira/config.php"
    point = 0

    driver.execute_script(f"window.open('{url_multib}');")

    # Click on Multibandeiras
    print(f"-- [{timestamp()}] Entrando em Mulibandeiras")

    driver.switch_to.window(driver.window_handles[1])

    while point == 0:
        driver.find_element(By.ID, "sd1").click()
        point = 1

    # Send input ID SiTef and search by
    try:
        search_id = driver.find_element(By.ID, 'ComboEmp_auto')
        search_id.clear()
        search_id.send_keys(id_sitef)
        time.sleep(2)
        search_id.send_keys(Keys.ENTER)
        print(f"-- [{timestamp()}] Pesquisando o ID Sitef: {id_sitef}")
        time.sleep(2)

    except Exception as e:
        send_message(f"Erro ao pesquisar ID Sitef! \n{e}")
        print(f"[{timestamp()}] Erro ao pesquisar ID Sitef! \n{e}")

    # Get all modules with logico
    point = 0

    while point == 0:
        try:
            target = '//table[@id="tabMB"]/tbody/tr'
            search_logicos = driver.find_elements(By.XPATH, f"{target}")
            list_modulos = []
            list_bandeiras = []
            list_autorizadores = []

            count = 0
            while count == 0:
                for n in search_logicos:
                    # print(n.tag_name, " = ", n.text)
                    if n.tag_name == "tr":
                        td_bandeira = n.find_elements(By.TAG_NAME, "td")[0]
                        td_autorizador = n.find_elements(By.TAG_NAME, "td")[1]

                        # To prepare list to excel file
                        list_bandeiras.append(td_bandeira.text)
                        list_autorizadores.append(td_autorizador.text)

                        # To print result
                        listar_logico = f"{td_bandeira.text}: {td_autorizador.text}"
                        list_modulos.append(listar_logico)
                        print("....", listar_logico)

                count = 1

            point = 1

        except Exception as e:
            send_message(f"Erro ao capturar lógicos da empresa! \n{e}")
            print(f"[{timestamp()}] Erro ao capturar lógicos da empresa! \n\n{e}")

    # Guardando CNPJ em variável
    try:
        get_cnpj = driver.find_elements(By.ID, 'LabelDadosEmpresa')
        for n in get_cnpj:
            # CNPJ = n.text
            CNPJ = n.text.replace("Nome: ", "")
            # print(f'----{CNPJ}')
    except Exception as e:
        print(f"[{timestamp()}] Erro ao capturar CNPJ da empresa! \n\n{e}")

    # Save to excel file
    point = 0
    while point == 0:
        try:
            print(f"-- [{timestamp()}] Exportando para Planilha")

            dic_multibandeiras = {'Bandeiras': list_bandeiras,
                                  'Autorizador': list_autorizadores}

            df_mb = pd.DataFrame(dic_multibandeiras)

            print(df_mb)

            # carrega o modelo do multibandeiras
            modelo_multibandeiras = f'{path_main}templates/Multibandeiras.xlsx'
            workbook = openpyxl.load_workbook(modelo_multibandeiras)
            # carrega a aba 1 da planilha, ou seja, Multibandeiras Novo
            sheet1 = workbook.worksheets[0]  # aba 0
            sheet2 = workbook.worksheets[1]  # aba 1

            # preenche as células
            c = 0
            print(f"-- [{timestamp()}] Inserindo bandeiras")
            for i in df_mb.index:
                sheet1['C1'].value = CNPJ
                sheet1_a2 = df_mb.iloc[c:c+1, :1].to_string(index=False,
                                                            header=None)
                sheet1_b2 = df_mb.iloc[c:c+1, 1:2].to_string(index=False,
                                                             header=None)
                sheet2_a3 = df_mb.iloc[c:c+1, :1].to_string(index=False,
                                                            header=None)
                sheet2_b3 = df_mb.iloc[c:c+1, 1:2].to_string(index=False, 
                                                             header=None)

                sheet1[f'A{c+1}'].value = sheet1_a2
                sheet1[f'B{c+1}'].value = sheet1_b2
                sheet2[f'A{c+2}'].value = sheet2_a3
                sheet2[f'B{c+2}'].value = sheet2_b3

                c += 1

            workbook.save(f'{path_main}downloads/Multibandeiras - {id_sitef}.xlsx')

            send_message(f"Multibandeiras {id_sitef} encerrado!")

            point = 1

        except Exception as e:
            send_message(f"Erro ao criar planilha! \n{e}")
            print(f"[{timestamp()}] Erro ao criar planilha! \n\n{e}")


if __name__ == "__main__":
    verify_path()
    get_idsitef()

    efetuar_login()
    acessar_configurador()
    consultar_multibandeiras(id_sitef)
    print("[FIM]")
    input()
