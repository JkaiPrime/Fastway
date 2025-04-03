from db.main import DatabaseCRUD

class DataService:
    def __init__(self):
        try:
            self.db = DatabaseCRUD()
        except Exception as e:
            print(f"Falha ao iniciar o serviço: {e}")
            self.db = None

    def create_entry(self, table, user, password, otp):
        """Valida e cria uma entrada no banco."""
        if not self.db:
            print("Erro: Banco de dados não inicializado.")
            return False
            
        if not all([user, password, otp]):
            print("Erro: Todos os campos são obrigatórios.")
            return False
            
        return self.db.insert_entry(table, user, password, otp)


    def get_entry(self, table, entry_id=None):
        """Retorna uma entrada específica ou todas as entradas da tabela."""
        return self.db.get_entries(table, entry_id)

    def update_entry(self, table, entry_id, user=None, password=None, otp=None):
        """Atualiza uma entrada na tabela."""
        if not any([user, password, otp]):
            raise ValueError("Pelo menos um campo (user, password, otp) deve ser fornecido.")
        return self.db.update_entry(table, entry_id, user, password, otp)

    def delete_entry(self, table, entry_id):
        """Exclui uma entrada da tabela."""
        return self.db.delete_entry(table, entry_id)

    def close_connection(self):
        """Fecha a conexão com o banco de dados."""
        self.db.close()