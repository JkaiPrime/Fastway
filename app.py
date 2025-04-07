import subprocess
import platform
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.Services.service_db import DataService


class FastWayApp:
    def __init__(self):
        self.db_service = DataService()
        
    def show_header(self):
        print("######################################################")
        print("#             FastWay - Tefway                       #")
        print("######################################################")
        print("#             Bem vindo ao FastWay                   #")
        print("######################################################")

    def show_menu(self):
        print("\nDigite a opção a utilizar do FastWay:")
        print("1 - Abrir Portal Software Express (Elgin)")
        print("2 - Abrir Portal Software Express (Comnect)")

        print("3 - Verificar vendas de usuário Elgin")
        print("4 - Verificar vendas de usuário Connect")
        print("5 - Cadastrar Credenciais de acesso")
        print("0 - Sair")

    def open_portal(self, server_type):
        """Abre o portal correspondente ao servidor especificado"""
        try:
            script_path = "src/fiserv_and_linx/express.py"
            command = f'python3 "{script_path}" {1 if server_type == "Elgin" else 2}'
            
            subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"\n✅ Portal {server_type} aberto com sucesso!")
            
        except Exception as e:
            print(f"\n❌ Erro ao abrir portal: {str(e)}")

    def send_tables(self, client_type):
        """Envia carga de tabelas para o cliente especificado"""
        print(f"\n⏳ Enviando tabelas para {client_type}...")
        # Implementação específica aqui

    def check_sales(self, company):
        """Verifica vendas de um usuário"""
        try:
            user_id = input("\nDigite o ID do usuário: ")
            sales = self.db_service.get_sales(company, user_id)
            print(f"\n📊 Vendas do usuário {user_id}:")
            print(sales)
        except Exception as e:
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
                print("\n✅ Credenciais cadastradas com sucesso!")
            else:
                print("\n❌ Falha no cadastro das credenciais!")

        except Exception as e:
            print(f"\n❌ Erro no cadastro: {str(e)}")

    def main(self):
        while True:
            self.show_header()
            self.show_menu()
            option = input("\nOpção: ").strip()

            match option:
                case "1": self.open_portal("Elgin")
                case "2": self.open_portal("Comnect")
                case "3": self.check_sales("Elgin")
                case "4": self.check_sales("Comnect")
                case "5": self.register_credentials()
                case "0": 
                    print("\n👋 Até logo!")
                    break
                case _: 
                    print("\n❌ Opção inválida!")

if __name__ == "__main__":
    try:
        app = FastWayApp()
        app.main()
    except KeyboardInterrupt:
        print("\n🛑 Aplicação interrompida pelo usuário!")
    except Exception as e:
        print(f"\n🔥 Erro crítico: {str(e)}")