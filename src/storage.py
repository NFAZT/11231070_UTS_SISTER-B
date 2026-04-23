import sqlite3

DB_NAME = "events.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS processed_events (
            event_id TEXT PRIMARY KEY,
            topic TEXT
        )
    """)
    conn.commit()
    conn.close()


def is_duplicate(event_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM processed_events WHERE event_id = ?", (event_id,))
    result = c.fetchone()
    conn.close()
    return result is not None


def save_event(event_id, topic):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO processed_events (event_id, topic) VALUES (?, ?)", (event_id, topic))
    conn.commit()
    conn.close()