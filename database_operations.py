import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            rank_points INTEGER NOT NULL,
            clan TEXT NOT NULL,
            last_updated TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_player(player_name, rank_points, clan):
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (player_name, rank_points, clan, last_updated) VALUES (?, ?, ?, ?)",
                   (player_name, rank_points, clan, datetime.now()))
    conn.commit()
    conn.close()

def get_player(player_name):
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute("SELECT player_name, rank_points, clan FROM players WHERE player_name = ?", (player_name,))
    player = cursor.fetchone()
    conn.close()
    return player

def update_player(player_name, rank_points, clan):
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE players SET rank_points = ?, clan = ?, last_updated = ? WHERE player_name = ?",
                   (rank_points, clan, datetime.now(), player_name))
    conn.commit()
    conn.close()

def delete_player(player_name):
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players WHERE player_name = ?", (player_name,))
    conn.commit()
    conn.close()

def get_leaderboard():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute("SELECT player_name, rank_points, clan FROM players ORDER BY rank_points DESC LIMIT 10")
    players = cursor.fetchall()
    conn.close()
    return players

def get_all_players():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute("SELECT player_name FROM players")
    players = cursor.fetchall()
    conn.close()
    return [player[0] for player in players]

def update_player_data(player_name, rank_points):
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE players SET rank_points = ?, last_updated = ? WHERE player_name = ?",
                   (rank_points, datetime.now(), player_name))
    conn.commit()
    conn.close()
