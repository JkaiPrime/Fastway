
import subprocess
import platform
from src.Services import service_db

def get_mac_address():
    sistema = platform.system()
    try:
        if sistema == "Windows":
            # Comando para Windows
            output = subprocess.check_output("getmac", text=True)
            mac = output.split()[0]  # Pega o primeiro MAC da lista
        elif sistema in ["Linux", "Darwin"]:  # Darwin = Mac
            # Comando para Linux/Mac
            output = subprocess.check_output(["ifconfig" if sistema == "Darwin" else "ip", "link"], text=True)
            for linha in output.split('\n'):
                if "link/ether" in linha:  # Linux
                    mac = linha.split()[1]
                    break
                elif "ether" in linha:  # Mac
                    mac = linha.split()[1]
                    break
        else:
            return None
        return mac.strip()
    except Exception as e:
        print("Erro:", e)
        return None



def main():
    db_service = service_db.DataService()
    print(get_mac_address())
    
    print("######################################################")
    print("#             FastWay - Tefway                       #")
    print("######################################################")
    print("#             Bem vindo ao FastWay                   #")
    print("######################################################")
    print("Digite a opção a utilizar do FastWay:")
    print("1 - Abrir o Portal da Software Express no servidor da Elgin")
    print("2 - Abrir o Portal da Software Express no servidor da Comnect")
    print("3 - Mandar carga de tabelas para um cliente Elgin")
    print("4 - Mandar carga de tabelas para um cliente Comnect")
    print("5 - Verificar vendas de um usuario da Elgin")
    print("6 - Verificar vendas de um usuario da Connect")
    print("7 - Cadastrar Crendenciais para acesso.")
    print("Caso queiram mais funcionalidades por favor nos contatar.")
    option = input("Digite a opção desejada: ")
    match option:
        case "1":
            print("Abrindo o Portal da Software Express no servidor da Elgin")
            # subprocess.call(["open", "http://38.0.101.76:8080/"])
        case "2":
            print("Abrindo o Portal da Software Express no servidor da Connect")
            # subprocess.call(["open", "http://38.0.101.76:8080/"])
        case "3":
            print("Mandando carga de tabelas para um cliente Elgin")
        case "4":
            print("Mandando carga de tabelas para um cliente Connect")
        case "5":
            print("Verificando vendas de um usuario da Elgin")
        case "6":
            print("Verificando vendas de um usuario da Connect")
        case "7":
            print("Cadastrar Crendenciais para acesso.")
            db_service.create_entry("Elgin", "lucas", "senha123", "987654")
            
        case _:
            print("Opção inválida, tente novamente.")
    
    entries = service_db.DataService().get_entry("Elgin")
    print("Entradas na Elgin:", entries)
    
if __name__ == "__main__":
    main()