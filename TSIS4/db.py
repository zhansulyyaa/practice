import psycopg2
from config import *

DB = dict(host="localhost", database="snake_db", user="postgres", password="postgres")

def get_conn():
    return psycopg2.connect(**DB)

def setup():
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id       SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id            SERIAL PRIMARY KEY,
            player_id     INTEGER REFERENCES players(id),
            score         INTEGER   NOT NULL,
            level_reached INTEGER   NOT NULL,
            played_at     TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    conn.close()

def get_or_create_player(username):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("INSERT INTO players(username) VALUES(%s) ON CONFLICT(username) DO NOTHING", (username,))
    conn.commit()
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    pid = cur.fetchone()[0]
    conn.close()
    return pid

def save_session(player_id, score, level):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(
        "INSERT INTO game_sessions(player_id, score, level_reached) VALUES(%s,%s,%s)",
        (player_id, score, level)
    )
    conn.commit()
    conn.close()

def get_top10():
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("""
        SELECT p.username, s.score, s.level_reached, s.played_at::date
        FROM game_sessions s
        JOIN players p ON p.id = s.player_id
        ORDER BY s.score DESC
        LIMIT 10
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_personal_best(player_id):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(
        "SELECT MAX(score) FROM game_sessions WHERE player_id = %s",
        (player_id,)
    )
    result = cur.fetchone()[0]
    conn.close()
    return result or 0
