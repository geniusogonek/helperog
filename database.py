import sqlite3


def init_tables():
    conn = sqlite3.connect("database.db")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY, 
        text text NOT NULL,
        answer text NOT NULL
    );
    """)


def add_request(text, answer):
    conn = sqlite3.connect("database.db")
    conn.execute(f"""
    INSERT INTO requests (
        text,
        answer
    ) VALUES (
        {text},
        {answer}
    );
    """)


def get_last_request():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT text, answer FROM requests LIMIT 1 OFFSET -1
    """)
    return cursor.fetchall()