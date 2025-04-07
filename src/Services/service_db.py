from db.database import DatabaseCRUD

class DataService:
    def __init__(self):
        self.db = DatabaseCRUD()

    def create_entry(self, table, user, password, otp):
        return self.db.insert_entry(table, user, password, otp)

    def update_entry(self, table, entry_id, user=None, password=None, otp=None):
        return self.db.update_entry(table, entry_id, user, password, otp)

    def get_entry(self, table, entry_id=None):
        return self.db.get_entries(table, entry_id)

    def delete_entry(self, table, entry_id):
        return self.db.delete_entry(table, entry_id)


    def get_credentials(self, server: int):
        """Busca credenciais no banco com tratamento de erros"""
        if not self.db:
            raise ConnectionError("Banco de dados não conectado")

        table = "Elgin" if server == 1 else "Connect"
        entries = self.db.get_entries(table)

        if not entries:
            raise ValueError(f"⚠️ Nenhuma credencial cadastrada para {table}!")

        # Valida estrutura dos dados
        if not all(key in entries[0] for key in ["user", "password", "otp"]):
            raise ValueError("Credenciais mal formatadas no banco")

        return (
            entries[0]["user"],
            entries[0]["password"],
            entries[0]["otp"]
    )


    def get_all_credentials(self):
        """Retorna todos os registros de user, password e otp das três tabelas."""
        return self.db.get_all_credentials()

    def close(self):
        self.db.close()

# Exemplo de uso
if __name__ == "__main__":
    service = DataService()
    
    print("\nCredenciais de todas as tabelas:")
    creds = service.get_all_credentials()
    for table, entries in creds.items():
        print(f"\nTabela: {table}")
        for entry in entries:
            print(f"User: {entry['user']}, Password: {entry['password']}, OTP: {entry['otp']}")
    
    service.close()
