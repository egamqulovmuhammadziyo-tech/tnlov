import sqlite3
import threading

local = threading.local()

def get_conn():
    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect("ovozlar.db", check_same_thread=False)
        local.conn.execute("PRAGMA journal_mode=WAL")
        local.conn.execute("PRAGMA synchronous=NORMAL")
        local.conn.execute("PRAGMA cache_size=10000")
    return local.conn

def db_create():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ovozlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            ustoz TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON ovozlar(user_id)")
    conn.commit()

def ovoz_bergan(user_id):
    conn = get_conn()
    cur = conn.execute("SELECT 1 FROM ovozlar WHERE user_id = ?", (user_id,))
    return cur.fetchone()

def ovoz_saqlash(user_id, ustoz):
    conn = get_conn()
    conn.execute("INSERT OR IGNORE INTO ovozlar (user_id, ustoz) VALUES (?, ?)", (user_id, ustoz))
    conn.commit()

def natijalar():
    conn = get_conn()
    cur = conn.execute("SELECT ustoz, COUNT(*) as son FROM ovozlar GROUP BY ustoz ORDER BY son DESC")
    return cur.fetchall()