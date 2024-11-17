import sqlite3


class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("database.db")

    def init_tables(self):
        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY, 
            text text NOT NULL,
            answer text NOT NULL,
            is_num BOOL NOT NULL
        );
        """)


    def add_request(self, text, answer, is_num=False):
        self.connection.execute(f"""
        INSERT INTO requests (text, answer, is_num) VALUES ('{text}', '{answer}', {str(is_num).lower()});
        """)
        self.connection.commit()


    def get_last_request(self):
        cursor = self.connection.cursor()
        cursor.execute("""
        SELECT text, answer FROM requests ORDER BY 0 - id LIMIT 1
        """)
        result = cursor.fetchone()
        cursor.close()
        return result


    def get_last_num(self):
        cursor = self.connection.cursor()
        cursor.execute("""
        SELECT answer FROM requests WHERE is_num = true ORDER BY 0 - id LIMIT 1
        """)
        result = cursor.fetchone()
        cursor.close()
        return result