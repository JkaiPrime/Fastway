import subprocess


def send_message(message):
    subprocess.Popen(['notify-send', message], )
    return


def verify_path():
    global path_main

    import os

    # To variable from Linux (autostart or terminal)
    path_main = f"{os.getcwd()}/"
    this_file = "carga_dtef.py"

    combine = f"{path_main}{this_file}"

    if os.path.exists(combine) is True:
        pass

    else:
        path_main = f"{path_main}TicketServer/"


def login():
    global driver, path_main

    # import os
    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    # from selenium.webdriver.common.action_chains import ActionChains

    https_login = "https://tef.linxsaas.com.br/tefweb/DTefWeb.cgi/login"

    send_message("Logando no Portal D-Tef")

    # Get credentials
    read_file = open(f"{path_main}sysfiles/authLinx.txt", "r").readlines()
    user = read_file[0].replace("\n", "")
    password = read_file[1]

    # Webdriver Configurations
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(https_login)

    # Loading login page
    while driver.current_url != https_login:
        time.sleep(1)

    # Inserting password and login
    search_box_login = driver.find_element(By.NAME, 'edtLogin')
    search_box_login.send_keys(user)
    search_box_passw = driver.find_element(By.NAME, 'edtSenha')
    search_box_passw.send_keys(password)
    # search_box_login.submit()

    # Loading home page
    count = 0

    # loading = driver.find_element(By.ID, 'ui-id-2')
    while count == 0:
        try:
            driver.find_element(By.ID, 'ui-id-2')
            count = 1
        except Exception:
            print("Carregando...")
            time.sleep(1)
        # driver.find_element(By.ID, 'ui-id-2')
        # loading = driver.find_element(By.ID, 'ui-id-2')

    # Closing Warning
    search_warning = driver.find_elements(By.TAG_NAME, "button")
    for n in search_warning:
        if n.text == "Fechar":
            n.click()


def get_cnpjs():  # OK
    global list_all_cnpj

    list_all_cnpj = []
    count = 0

    # Get credentials
    read_file = open(f"{path_main}sysfiles/reqCnpj.txt", "r").readlines()
    for n in read_file:
        if count == 0:
            cnpj = read_file[count].replace("\n", "")
            list_all_cnpj.append(cnpj)
            count += 1
        else:
            cnpj = read_file[count].replace("\n", "")
            list_all_cnpj.append(cnpj)
            count += 1
        # user = read_file[0].replace("\n", "")
        # password = read_file[1]
    # print(list_all_cnpj)


def load_monitoracao(find_cnpj):
    import time
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait  # to change to iframe
    from selenium.webdriver.support import expected_conditions as EC  # to change to iframe

    # Loading monitoração page
    search_menu_monitoracao = driver.find_elements(By.TAG_NAME, "a")
    for n in search_menu_monitoracao:
        if n.text == "Monitoração":
            n.click()

            # Loading loja page
            search_menu_loja = driver.find_elements(By.LINK_TEXT, "Loja")
            for n2 in search_menu_loja:
                n2.click()
                time.sleep(5)

    # Clicking on Loja
    try:
        target = '//div[@id="DIV_frameDinamico"]/iframe'
        WebDriverWait(driver,20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, target)))
        div = driver.find_element(By.XPATH, '//div[@class="seletor-loja"]/seletor-loja/span/span/span')
        div.click()
        time.sleep(2)
    except Exception as e:
        print(f"\nErro ao Clicar em Loja: \n{e}")

    # Send CNPJ to input
    try:
        cnpj = find_cnpj  # get cnpj from lista_cnpj.txt
        search_cnpj = driver.find_element(By.CLASS_NAME, "select2-search__field")
        search_cnpj.send_keys(cnpj)
        time.sleep(5)
    except Exception as e:
        print(f"\nErro ao Enviar CNPJ: \n{e}")

    # Click to load
    try:
        select_cnpj = driver.find_elements(By.TAG_NAME, "item-lista-estrut-org")[1]
        var_empresa = select_cnpj.get_attribute("nome")
        print(f"\nCNPJ: {cnpj} \nNome: {var_empresa}")
        # select_cnpj.send_keys()
        select_cnpj_2 = driver.find_elements(By.CLASS_NAME, "id-estrut-org")[1]
        select_cnpj_2.click()
        time.sleep(3)
    except Exception as e:
        print(f"\nErro ao Selecionar CNPJ: \n{e}")

    # Get variables
    count = 0
    count_ini = 0

    lines = driver.find_elements(By.XPATH, '//table[@id="table_tabela_redes"]/tbody/tr')

    for n in lines:

        if count % 2 != 0:

            try:
                search_autorizador = driver.find_elements(By.XPATH, '//table[@id="table_tabela_redes"]/tbody/tr')[count]
                search_autorizador_2 = search_autorizador.find_elements(By.TAG_NAME, "td")

                # Find more than one autorizador
                line_autorizador = []
                for n in search_autorizador_2:
                    line_autorizador.append(n.text.strip())

                print(f"\nAutorizador: {line_autorizador[0]}",
                      f"\nLógico: {line_autorizador[1]}",
                      f"\nStatus: {line_autorizador[2]}")

                # Click on "Inicializar"
                try:
                    # search_ini = line_autorizador[3]
                    search_ini = driver.find_elements(By.LINK_TEXT, "Inicializar")[count_ini]
                    search_ini.click()
                    time.sleep(2)
                    texto_final = f"Carga {line_autorizador[0]} aplicada com sucesso!"
                    send_message(texto_final)

                except Exception as e:
                    print(f"\nErro ao Clicar em Inicializar: \n{e}")

                count_ini += 1

            except Exception as e:
                print(f"\nErro ao obter dados do Autorizador: \n{e}")

            count += 1

        else:
            count += 1

    time.sleep(10)


def load_monitoracao_continue(find_cnpj):
    import time
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait  # to change to iframe
    from selenium.webdriver.support import expected_conditions as EC  # to change to iframe

    # Clicking on Loja
    try:
        target = '//div[@id="DIV_frameDinamico"]/iframe'
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, target)))
        div = driver.find_element(By.XPATH, '//div[@class="seletor-loja"]/seletor-loja/span/span/span')
        div.click()
        time.sleep(2)
    except Exception as e:
        print(f"\nErro ao Clicar em Loja: \n{e}")

    # Send CNPJ to input
    try:
        cnpj = find_cnpj  # get cnpj from lista_cnpj.txt
        search_cnpj = driver.find_element(By.CLASS_NAME, "select2-search__field")
        search_cnpj.send_keys(cnpj)
        time.sleep(5)
    except Exception as e:
        print(f"\nErro ao Enviar CNPJ: \n{e}")

    # Click to load
    try:
        select_cnpj = driver.find_elements(By.TAG_NAME, "item-lista-estrut-org")[1]
        var_empresa = select_cnpj.get_attribute("nome")
        print(f"\nCNPJ: {cnpj} \nNome: {var_empresa}")
        # select_cnpj.send_keys()
        select_cnpj_2 = driver.find_elements(By.CLASS_NAME, "id-estrut-org")[1]
        select_cnpj_2.click()
        time.sleep(3)
    except Exception as e:
        print(f"\nErro ao Selecionar CNPJ: \n{e}")

    # Get variables
    try:
        search_autorizador = driver.find_elements(By.XPATH, '//table[@id="table_tabela_redes"]/tbody/tr')[1]
        search_autorizador_2 = search_autorizador.find_elements(By.TAG_NAME, "td")

        # Find more than one autorizador
        line_autorizador = []
        for n in search_autorizador_2:
            line_autorizador.append(n.text.strip())

        print(f"\nAutorizador: {line_autorizador[0]}",
              f"\nLógico: {line_autorizador[1]}",
              f"\nStatus: {line_autorizador[2]}")

    except Exception as e:
        print(f"\nErro ao obter dados do Autorizador: \n{e}")

    # # Click on "Inicializar"
    # try:
    #     search_ini = driver.find_element(By.LINK_TEXT, "Inicializar")
    #     search_ini.click()
    #     print("Carga aplicada com sucesso")
    # except Exception as e:
    #     print(f"\nErro ao Clicar em Inicializar: \n{e}")

    # Freeze time
    time.sleep(2)


if __name__ == "__main__":
    verify_path()
    get_cnpjs()

    for i in list_all_cnpj:
        login()
        load_monitoracao(i)
