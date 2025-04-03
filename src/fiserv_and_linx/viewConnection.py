def viewConnections():
    global path_main, getCnpj
    import webbrowser  # para abrir o navegador
    import os
    import subprocess  # para notificar no Linux

    path_main = f"{os.getcwd()}/"
    this_file = "viewConnection.py"

    # função para enviar notificações para o Linux
    def sendmessage(message):
        subprocess.Popen(['notify-send', message])
        return

    # Verifying path to change directory
    def verify_path():
        global path_main
        combine = f"{path_main}{this_file}"

        if os.path.exists(combine) is True:
            pass

        else:
            path_main = f"{path_main}TicketServer/"

    def standardzation_cnpj():
        global getCnpj
        # Verify if CNPJ has mask and converto to standard (with mask)
        string_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        drop_list = []

        if len(getCnpj) != 14:
            count = 0

            # Put in list characters
            for i in getCnpj:

                if i in string_numbers:
                    pass

                else:
                    drop_list.append(getCnpj[count])

                count += 1

            # Remove each character
            count_n = 0
            for n in drop_list:
                getCnpj = getCnpj.replace(drop_list[count_n], "")
                count_n += 1

        elif len(getCnpj) == 14:
            pass

        else:
            return f"O CNPJ {getCnpj} não segue o padrão de estar com máscara ou sem."

    verify_path()

    # getCnpj = easygui.enterbox("Insira o CNPJ sem pontuação.")
    reqCnpjR = open(f"{path_main}sysfiles/reqCnpj.txt", "r")
    getCnpj = reqCnpjR.read()

    standardzation_cnpj()

    # variável url comnect
    url_base1 = f"https://meutef.tefway.com.br/customers?utf8=%E2%9C%93&direction=&sort=&show_all=&status=&nome=&cnpj={getCnpj}"
    url_base2 = f'https://tefway.app.gluocrm.com.br/index.php?module=VPNTefway&parent=&page=1&view=List&viewname=495&orderby=&sortorder=&app=SUPPORT&search_params=%5B%5B%5B%22chave%22%2C%22c%22%2C%22{getCnpj}%22%5D%5D%5D&tag_params=%5B%5D&nolistcache=0&list_headers=%5B%22chave%22%2C%22account_id%22%2C%22cf_2219%22%2C%22cf_2170%22%2C%22cf_2079%22%2C%22ip_real%22%2C%22accountsrel%22%2C%22servicecontractsid%22%2C%22productid%22%2C%22sistema_operacional_vpntefway%22%2C%22disponibilidade_vpntefway%22%2C%22assigned_user_id%22%5D&tag='

    webbrowser.open(url_base1, new=1, autoraise=True)  # para abrir no browser os chamados
    webbrowser.open(url_base2, new=0, autoraise=True)  # para abrir no browser os chamados

    os.remove(f"{path_main}sysfiles/reqCnpj.txt")


if __name__ == "__main__":
    viewConnections()
