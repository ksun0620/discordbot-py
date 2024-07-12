import sqlite3

def update_database():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    
    # players 테이블에 누락된 컬럼이 있는지 확인하고 추가
    try:
        cursor.execute("ALTER TABLE players ADD COLUMN clan TEXT DEFAULT '[SSIB]'")
        print("Column 'clan' added successfully.")
    except sqlite3.OperationalError:
        print("Column 'clan' already exists.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_database()
