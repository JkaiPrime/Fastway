import sqlite3
import os
import platform
from cryptography.fernet import Fernet

class DatabaseCRUD:
    def __init__(self, db_name=None):
        self.system = platform.system()
        self.base_path = self._get_base_path()
        os.makedirs(self.base_path, exist_ok=True)
        self.db_name = db_name or os.path.join(self.base_path, "database.db")
        self.key_path = os.path.join(self.base_path, "secret.key")
        self.fernet = self._load_or_create_key()
        self.connection = None
        self.cursor = None

        os.makedirs(self.base_path, exist_ok=True)
        self._connect()
        self.create_tables()

    def _get_base_path(self):
        if self.system == "Windows":
            return "C:/Fastway"
        else:
            return os.path.join(os.path.expanduser("~"), ".fastway")

    def _load_or_create_key(self):
        if not os.path.exists(self.key_path):
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as key_file:
                key_file.write(key)
            #print(f"🔐 Nova chave secreta gerada em: {self.key_path}")
        else:
            #print(f"🔐 Usando chave existente de: {self.key_path}")
            pass

        with open(self.key_path, "rb") as key_file:
            return Fernet(key_file.read())

    def _encrypt(self, text):
        return self.fernet.encrypt(text.encode()).decode()

    def _decrypt(self, text):
        return self.fernet.decrypt(text.encode()).decode()

    def _connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def close(self):
        if self.connection:
            self.connection.close()

    def create_tables(self):
        for table in ["Elgin", "Comnect", "Tefway"]:
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT NOT NULL,
                    password TEXT NOT NULL,
                    otp TEXT NOT NULL
                )
            """)
        self.connection.commit()

    def insert_entry(self, table, user, password, otp):
        try:
            self.cursor.execute(f"""
                INSERT INTO {table} (user, password, otp)
                VALUES (?, ?, ?)
            """, (
                self._encrypt(user),
                self._encrypt(password),
                self._encrypt(otp)
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao inserir dados: {e}")
            return False

    def get_entries(self, table, entry_id=None):
        try:
            if entry_id:
                self.cursor.execute(f"SELECT * FROM {table} WHERE id=?", (entry_id,))
            else:
                self.cursor.execute(f"SELECT * FROM {table}")
            rows = self.cursor.fetchall()
            return [
                {
                    "id": row["id"],
                    "user": self._decrypt(row["user"]),
                    "password": self._decrypt(row["password"]),
                    "otp": self._decrypt(row["otp"])
                }
                for row in rows
            ]
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
            return []

    def update_entry(self, table, entry_id, user=None, password=None, otp=None):
        try:
            fields = []
            values = []

            if user:
                fields.append("user = ?")
                values.append(self._encrypt(user))
            if password:
                fields.append("password = ?")
                values.append(self._encrypt(password))
            if otp:
                fields.append("otp = ?")
                values.append(self._encrypt(otp))

            values.append(entry_id)

            sql = f"UPDATE {table} SET {', '.join(fields)} WHERE id = ?"
            self.cursor.execute(sql, tuple(values))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar entrada: {e}")
            return False

    def delete_entry(self, table, entry_id):
        try:
            self.cursor.execute(f"DELETE FROM {table} WHERE id = ?", (entry_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar entrada: {e}")
            return False

    def get_all_credentials(self):
        data = {}
        for table in ["Elgin", "Comnect", "Tefway"]:
            data[table] = self.get_entries(table)
        return data
