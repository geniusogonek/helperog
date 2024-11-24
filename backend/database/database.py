import sqlite3
import bcrypt


class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("database/database.db")

    def create_tables(self):
        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY_KEY AUTO_INCREMENT,
            username varchar(255) UNIQUE NOT NULL,
            hash_password varchar(255) NOT NULL,
            token_used INTEGER DEFAULT 0
        )
        """)
        self.connection.commit()

    def register_user(self, username, password):
        try:
            hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(4))
            self.connection.execute(f"INSERT INTO users (username, hash_password) VALUES ('{username}', '{hash_password}')")
            self.connection.commit()
            return True
        except:
            return False

    def login_user(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT hash_password FROM users WHERE username = '{username}'")
        hash_password = cursor.fetchone()
        cursor.close()
        if hash_password:
            return bcrypt.checkpw(password.encode("utf-8"), hash_password.encode("utf-8"))
        return False

    def get_token_used(self, username):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT token_used FROM users WHERE username = '{username}'")
        res = cursor.fetchone()[0]
        cursor.close()
        return res

    def increase_token_used(self, username, token_count):
        token_used = self.get_token_used(username) + token_count
        self.connection.execute(f"UPDATE users SET token = {token_used} WHERE username = '{username}'")
