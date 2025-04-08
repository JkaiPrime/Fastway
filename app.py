import subprocess
import sys
import os
from src.utils import logger
import src.fiserv_and_linx.express as express
import src.fiserv_and_linx.relatorio_express as relatorio
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from src.Services.service_db import DataService


class FastWayApp:
    def __init__(self):
        logger.info("Inicializando FastWayApp")
        self.db_service = DataService()
        logger.info("Serviço de banco de dados carregado")

    def show_header(self):
        print("######################################################")
        print("#             FastWay - Tefway                       #")
        print("######################################################")
        print("#             Bem vindo ao FastWay                   #")
        print("######################################################")
        logger.info("Exibindo cabeçalho do sistema")

    def show_menu(self):
        print("\nDigite a opção a utilizar do FastWay:")
        print("1 - Abrir Portal Software Express (Elgin)")
        print("2 - Abrir Portal Software Express (Comnect)")
        print("3 - Verificar vendas de usuário Elgin")
        print("4 - Verificar vendas de usuário Connect")
        print("5 - Cadastrar Credenciais de acesso")
        print("0 - Sair")
        logger.info("Exibindo menu de opções")

    def open_portal(self, server_type):
        """Abre o portal correspondente ao servidor especificado"""
        try:
            express.run(server_type)



        except Exception as e:
            logger.error(f"Erro ao abrir portal {server_type}: {str(e)}")
            print(f"\n❌ Erro ao abrir portal: {str(e)}")

    def send_tables(self, client_type):
        """Envia carga de tabelas para o cliente especificado"""
        print(f"\n⏳ Enviando tabelas para {client_type}...")
        logger.info(f"Enviando tabelas para {client_type}...")
        # Implementação específica aqui

    def check_sales(self, company):
        """Verifica vendas de um usuário"""
        try:
            cnpj = input("\nDigite o cnpj do cliente: ")

            relatorio.run(cnpj_client=cnpj, server_desc=company)
            logger.info(f"Consulta de vendas para usuário {cnpj} da empresa {company}")
        except Exception as e:
            logger.error(f"Erro ao consultar vendas: {str(e)}")
            print(f"\n❌ Erro na consulta: {str(e)}")

    def register_credentials(self):
        """Cadastra novas credenciais de acesso"""
        try:
            print("\n📝 Cadastro de Credenciais")
            empresa = input("Empresa (Elgin/Comnect/Tefway): ").capitalize()
            usuario = input("Usuário: ").strip()
            senha = input("Senha: ").strip()
            otp = input("OTP: ").strip()

            if not all([empresa, usuario, senha, otp]):
                raise ValueError("Todos os campos são obrigatórios!")

            success = self.db_service.create_entry(
                table=empresa,
                user=usuario,
                password=senha,
                otp=otp
            )

            if success:

                logger.info(f"Credenciais cadastradas com sucesso para empresa: {empresa}")
            else:

                logger.warning(f"Falha no cadastro das credenciais para empresa: {empresa}")

        except Exception as e:
            logger.error(f"Erro no cadastro de credenciais: {str(e)}")
            print(f"\n❌ Erro no cadastro: {str(e)}")

    def main(self):
        while True:
            self.show_header()
            self.show_menu()
            option = input("\nOpção: ").strip()
            logger.info(f"Opção selecionada: {option}")

            match option:
                case "1": self.open_portal(1)
                case "2": self.open_portal(2)
                case "3": self.check_sales("Elgin")
                case "4": self.check_sales("Comnect")
                case "5": self.register_credentials()
                case "0": 
                    logger.info("Encerrando aplicação.")
                    print("\n👋 Até logo!")
                    break
                case _: 
                    logger.warning(f"Opção inválida: {option}")
                    print("\n❌ Opção inválida!")

if __name__ == "__main__":
    try:
        logger.info("Iniciando execução principal do FastWayApp")
        app = FastWayApp()
        app.main()
    except KeyboardInterrupt:
        logger.info("Execução interrompida pelo usuário.")
        print("\n🛑 Aplicação interrompida pelo usuário!")
    except Exception as e:
        logger.critical(f"Erro crítico na execução do aplicativo: {str(e)}")
        print(f"\n🔥 Erro crítico: {str(e)}")
