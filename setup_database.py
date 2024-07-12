import sqlite3

def create_database():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        player_name TEXT PRIMARY KEY,
        rank_points INTEGER,
        clan TEXT,
        last_updated TEXT
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database and table have been created successfully.")
