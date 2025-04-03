import http.client
import json
import webbrowser  # para abrir o navegador
import os  # para pegar o nome do arquivo
import re

path_main = f"{os.getcwd()}/"
this_file = "viewPedidos.py"


# Verifying path to change directory
def verify_path():
    global path_main
    combine = f"{path_main}{this_file}"

    if os.path.exists(combine) is True:
        pass

    else:
        path_main = f"{path_main}TicketServer/"


def standardzation_cnpj():
    global varcnpj
    # Verify if CNPJ has mask and converto to standard (with mask)
    string_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    drop_list = []

    if len(varcnpj) == 18:
        count = 0

        # Put in list characters
        for i in varcnpj:

            if i in string_numbers:
                pass

            else:
                drop_list.append(varcnpj[count])

            count += 1

        # Remove each character
        count_n = 0
        for n in drop_list:
            varcnpj = varcnpj.replace(drop_list[count_n], "")
            count_n += 1

        # Insert again mask
        cnpj_full = varcnpj[:2] + '.' + varcnpj[2:5]
        cnpj_full = cnpj_full + '.' + varcnpj[5:8]
        cnpj_full = cnpj_full + '/' + varcnpj[8:12]
        cnpj_full = cnpj_full + '-' + varcnpj[12:14]
        varcnpj = cnpj_full

    elif len(varcnpj) == 14:
        cnpj_full = varcnpj[:2] + '.' + varcnpj[2:5]
        cnpj_full = cnpj_full + '.' + varcnpj[5:8]
        cnpj_full = cnpj_full + '/' + varcnpj[8:12]
        cnpj_full = cnpj_full + '-' + varcnpj[12:14]
        varcnpj = cnpj_full

    else:
        print(f"O CNPJ {varcnpj} não segue o padrão de estar com máscara ou sem.")


verify_path()

reqCnpjFR = open(f"{path_main}sysfiles/reqCnpj.txt", "r")
varcnpj = reqCnpjFR.read()

standardzation_cnpj()

# #########  Capturando variavel CLIENTE via API ##########
"""VALIDAR SESSAO CRM"""


def get_session():
    import hashlib
    import json
    import http.client

    # getchallenge

    conn = http.client.HTTPSConnection("tefway.app.gluocrm.com.br")
    payload = ''
    headers = {}
    conn.request("GET", "/webservice.php?operation=getchallenge&username=portal", payload, headers)
    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))
    # print()

    data_dict_1 = json.loads(data)
    tokena = (data_dict_1["result"]["token"])
    # print(tokena)
    # print()

    two = (tokena + "PIaalh23f7KB9G38")
    # print(two)
    # print()
    # token + acess key --> md5 encode

    # initializing string
    str2hash = f"{two}"

    # encoding GeeksforGeeks using encode()
    # then sending to md5()
    result = hashlib.md5(str2hash.encode())

    # printing the equivalent hexadecimal value.
    # print("The hexadecimal equivalent of hash is : ", end="")
    # print(result.hexdigest())

    key = (result.hexdigest())
    # print(key)
    # print()

    #
    # # login

    import hashlib
    # import requests
    import json
    import http.client

    # getchallenge

    conn = http.client.HTTPSConnection("tefway.app.gluocrm.com.br")
    payload = ''
    headers = {}
    conn.request("GET",
                 "/webservice.php?operation=getchallenge&username=portal",
                 payload, headers)
    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))
    # print()

    data_dict_1 = json.loads(data)
    tokena = (data_dict_1["result"]["token"])
    # print(tokena)

    two = (tokena + "PIaalh23f7KB9G38")
    # print(two)
    # print()
    # token + acess key --> md5 encode

    # initializing string
    str2hash = f"{two}"

    # encoding GeeksforGeeks using encode()
    # then sending to md5()
    result = hashlib.md5(str2hash.encode())

    # printing the equivalent hexadecimal value.
    # print("The hexadecimal equivalent of hash is : ", end="")
    # print(result.hexdigest())
    # print()

    key = (result.hexdigest())
    # print(key)
    # print()
    #
    # # login

    import http.client
    # import mimetypes
    from codecs import encode

    conn = http.client.HTTPSConnection("tefway.app.gluocrm.com.br")
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=operation;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("login"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=username;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("portal"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=accessKey;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(f"{key}"))
    dataList.append(encode('--' + boundary + '--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    conn.request("POST", "/webservice.php", payload, headers)
    res = conn.getresponse()
    data_s = res.read()
    # print(data_s.decode("utf-8"))
    # print()

    data_dict_2 = json.loads(data_s)
    session = (data_dict_2["result"]["sessionName"])
    print(f"sessão iniciada: {session}")

    with open("session.txt", "w", encoding="utf-8") as arquivo:
        frases = list()
        frases.append(f"{session}")
        arquivo.writelines(frases)


get_session()

# inicia sessão
with open("session.txt", "r", encoding="utf-8") as arquivo:
    sessions = arquivo.readlines()
    for i, linha in enumerate(sessions):
        if i == 0:
            session = linha

# Pegar ID do CNPJ [metodo QUERY]

conn = http.client.HTTPSConnection("tefway.app.gluocrm.com.br")
payload = ''
headers = {}
conn.request("GET", f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM%20Accounts%20WHERE%20cpfcnpj='{varcnpj}';&=", payload, headers)
res = conn.getresponse()
data = res.read()

data_dict = json.loads(data)
id = (data_dict["result"][0]["id"])

# String original
string_original = id

# Usando expressão regular para extrair os dígitos após o 'x'
match = re.search(r'x(\d+)', string_original)

# Verificando se há correspondência
if match:
    # Obtendo a parte correspondente da string
    digitos = match.group(1)
    # print('Dígitos extraídos:', digitos)
    record = digitos
else:
    print('Nenhum dígito encontrado.')

os.remove('session.txt')

##########################################

url = f"https://tefway.app.gluocrm.com.br/index.php?module=Accounts&relatedModule=SalesOrder&view=Detail&record={record}&mode=showRelatedList&relationId=4&tab_label=Sales%20Order&app=MARKETING"

webbrowser.open(url, new=0, autoraise=True)  # para abrir no navegador

os.remove(f"{path_main}sysfiles/reqCnpj.txt")
