import sqlite3
import os
from sqlite3 import Error

class DatabaseCRUD:
    def __init__(self, db_name='db/database.db'):
        self.db_name = db_name
        self.connection = None
        try:
            # Cria o diretório se não existir
            os.makedirs(os.path.dirname(self.db_name), exist_ok=True)
            
            # Conecta ao banco de dados
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row
            print(f"Conexão com {self.db_name} estabelecida.")
            
            # Cria as tabelas
            self.create_tables()
            
        except Error as e:
            print(f"Erro crítico ao inicializar o banco: {e}")
            raise  # Propaga a exceção para interromper a execução

    def create_tables(self):
        """Cria as tabelas Elgin, Connect e Tefway."""
        try:
            cursor = self.connection.cursor()
            tables = ["Elgin", "Connect", "Tefway"]
            for table in tables:
                cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {table} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user TEXT NOT NULL,
                        password TEXT NOT NULL,
                        otp TEXT NOT NULL
                    )
                ''')
            self.connection.commit()
            print("Tabelas verificadas/criadas com sucesso!")
            
        except Error as e:
            print(f"Erro ao criar tabelas: {e}")
            raise

# database.py
    def insert_entry(self, table, user, password, otp):
        try:
            print(f"Tentando inserir em {table}: {user}, {password}, {otp}")
            cursor = self.connection.cursor()
            cursor.execute(f'''
                INSERT INTO {table} (user, password, otp)
                VALUES (?, ?, ?)
            ''', (user, password, otp))
            self.connection.commit()
            print("Inserção bem-sucedida!")
            return True
        except Error as e:
            print(f"Erro na inserção: {str(e)}")
            return False

    def update_entry(self, table, entry_id, user=None, password=None, otp=None):
        """Atualiza uma entrada pelo ID na tabela especificada."""
        try:
            cursor = self.connection.cursor()
            updates = []
            params = []
            
            if user:
                updates.append("user = ?")
                params.append(user)
            if password:
                updates.append("password = ?")
                params.append(password)
            if otp:
                updates.append("otp = ?")
                params.append(otp)
            
            if not updates:
                print("Nada para atualizar.")
                return False
            
            query = f"UPDATE {table} SET {', '.join(updates)} WHERE id = ?"
            params.append(entry_id)
            
            cursor.execute(query, params)
            self.connection.commit()
            print(f"Entrada {entry_id} atualizada na tabela {table}!")
            return True
        except Error as e:
            print(f"Erro ao atualizar entrada: {e}")
            return False

    def get_entries(self, table, entry_id=None):
        """Retorna todas as entradas ou uma específica (por ID) da tabela."""
        try:
            cursor = self.connection.cursor()
            if entry_id:
                cursor.execute(f"SELECT * FROM {table} WHERE id = ?", (entry_id,))
                result = cursor.fetchone()
                return dict(result) if result else None
            else:
                cursor.execute(f"SELECT * FROM {table}")
                return [dict(row) for row in cursor.fetchall()]
        except Error as e:
            print(f"Erro ao ler entradas: {e}")
            return []

    def get_all_credentials(self):
        """Retorna todos os registros de user, password e otp das tabelas Elgin, Connect e Tefway."""
        try:
            credentials = {}
            tables = ["Elgin", "Connect", "Tefway"]
            for table in tables:
                entries = self.get_entries(table)
                credentials[table] = [
                    {"user": e["user"], "password": e["password"], "otp": e["otp"]}
                    for e in entries
                ]
            return credentials
        except Error as e:
            print(f"Erro ao buscar credenciais: {e}")
            return {}

    def delete_entry(self, table, entry_id):
        """Exclui uma entrada pelo ID da tabela."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE id = ?", (entry_id,))
            self.connection.commit()
            print(f"Entrada {entry_id} excluída da tabela {table}!")
            return True
        except Error as e:
            print(f"Erro ao excluir entrada: {e}")
            return False

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.connection:
            self.connection.close()
            print("Conexão fechada.")

# Exemplo de uso
if __name__ == "__main__":

    db = DatabaseCRUD(db_name='db/database.db')
    
    if db.connection:  # Só opera se a conexão foi bem-sucedida
        db.insert_entry("Elgin", "user1", "pass123", "111111")
        print(db.get_entries("Elgin"))
    
    # Inserir dados
    db.insert_entry("Elgin", "user1", "pass123", "111111")
    db.insert_entry("Connect", "admin", "admin456", "222222")
    
    # Atualizar dados
    db.update_entry("Elgin", 1, password="nova_senha")
    
    # Ler dados
    print("\nTodos os dados da Elgin:")
    print(db.get_entries("Elgin"))
    
    print("\nEntrada com ID 1 da Connect:")
    print(db.get_entries("Connect", 1))

    # Obter todas as credenciais
    print("\nCredenciais completas:")
    print(db.get_all_credentials())
    
    # Excluir dados
    db.delete_entry("Elgin", 1)
    
    db.close()
