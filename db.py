import sqlite3


if __name__ == "__main__":
    conn = sqlite3.connect('data.db')
    us10y_vix = """
    CREATE TABLE IF NOT EXISTS us10y_vix (created_at DATETIME NOT NULL, data JSON NOT NULL);
    """
    conn.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nome TEXT, idade INTEGER)')
