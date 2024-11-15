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
    INSERT INTO requests (text, answer) VALUES ('{text}', '{answer}');
    """)
    conn.commit()


def get_last_request():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM requests ORDER BY 0 - id LIMIT 1
    """)
    return cursor.fetchall()

if __name__ == "__main__":
    add_request("last", "last")
    print(get_last_request())