import sqlite3


DB_FILE = "storyweaver.db"




def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS drafts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    outline TEXT,
    draft TEXT,
    style TEXT,
    tone TEXT,
    pacing TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()




def save_draft(title, outline, draft, style, tone, pacing):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO drafts (title, outline, draft, style, tone, pacing) VALUES (?, ?, ?, ?, ?, ?)",
    (title, outline, draft, style, tone, pacing))
    conn.commit()
    conn.close()

