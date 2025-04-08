from src.database import DatabaseCRUD
from src.utils import logger

class DataService:
    def __init__(self):
        logger.info("Inicializando DataService")
        self.db = DatabaseCRUD()
        logger.info("Instância de DatabaseCRUD criada")

    def create_entry(self, table, user, password, otp):
        logger.info(f"Criando entrada na tabela {table} para usuário {user}")
        return self.db.insert_entry(table, user, password, otp)

    def update_entry(self, table, entry_id, user=None, password=None, otp=None):
        logger.info(f"Atualizando entrada ID {entry_id} na tabela {table}")
        return self.db.update_entry(table, entry_id, user, password, otp)

    def get_entry(self, table, entry_id=None):
        logger.info(f"Buscando entrada{' ID ' + str(entry_id) if entry_id else ''} na tabela {table}")
        return self.db.get_entries(table, entry_id)

    def delete_entry(self, table, entry_id):
        logger.info(f"Deletando entrada ID {entry_id} da tabela {table}")
        return self.db.delete_entry(table, entry_id)

    def get_credentials(self, server: int):
        """Busca credenciais no banco com tratamento de erros"""
        if not self.db:
            logger.error("Tentativa de acessar o banco de dados sem conexão ativa")
            raise ConnectionError("Banco de dados não conectado")

        table = "Elgin" if server == 1 else "Comnect"
        logger.info(f"Buscando credenciais para servidor: {table}")
        entries = self.db.get_entries(table)

        if not entries:
            logger.warning(f"Nenhuma credencial encontrada para {table}")
            raise ValueError(f"⚠️ Nenhuma credencial cadastrada para {table}!")

        if not all(key in entries[0] for key in ["user", "password", "otp"]):
            logger.error("Credenciais mal formatadas encontradas no banco")
            raise ValueError("Credenciais mal formatadas no banco")

        return (
            entries[0]["user"],
            entries[0]["password"],
            entries[0]["otp"]
        )

    def get_all_credentials(self):
        logger.info("Buscando todas as credenciais em todas as tabelas")
        return self.db.get_all_credentials()

    def close(self):
        logger.info("Encerrando conexão com o banco de dados")
        self.db.close()


# Exemplo de uso
if __name__ == "__main__":
    service = DataService()
    logger.info("Executando exemplo de uso do DataService")

    print("\nCredenciais de todas as tabelas:")
    creds = service.get_all_credentials()
    for table, entries in creds.items():
        print(f"\nTabela: {table}")
        for entry in entries:
            print(f"User: {entry['user']}, Password: {entry['password']}, OTP: {entry['otp']}")

    service.close()
