import sqlite3


def init_tables():
    conn = sqlite3.connect("database.db")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY, 
        text text NOT NULL,
        answer text NOT NULL,
        is_num BOOL NOT NULL
    );
    """)


def add_request(text, answer, is_num=False):
    conn = sqlite3.connect("database.db")
    conn.execute(f"""
    INSERT INTO requests (text, answer, is_num) VALUES ('{text}', '{answer}', {str(is_num).lower()});
    """)
    conn.commit()


def get_last_request():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT text, answer FROM requests ORDER BY 0 - id LIMIT 1
    """)
    return cursor.fetchone()


def get_last_num():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT answer FROM requests WHERE is_num = true ORDER BY 0 - id LIMIT 1
    """)
    return cursor.fetchone()


if __name__ == "__main__":
    init_tables()
    #add_request("test", "test2", False)
    print(get_last_num())