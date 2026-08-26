import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path("data/content.db")

class MemoryDB:
    def __init__(self, path=DB_PATH):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.init()

    def init(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            topic TEXT NOT NULL,
            angle TEXT NOT NULL,
            keywords TEXT NOT NULL,
            content TEXT NOT NULL,
            hashtags TEXT NOT NULL,
            fingerprint TEXT NOT NULL,
            published_at TEXT NOT NULL,
            platform TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TEXT NOT NULL,
            status TEXT NOT NULL,
            message TEXT
        );
        """)
        self.conn.commit()

    def recent_posts(self, limit=1000):
        return self.conn.execute(
            "SELECT * FROM posts ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()

    def add_post(self, post, platform):
        self.conn.execute("""
            INSERT INTO posts(title, topic, angle, keywords, content, hashtags,
                               fingerprint, published_at, platform)
            VALUES(?,?,?,?,?,?,?, ?,?)
        """, (
            post["title"], post["topic"], post["angle"], ",".join(post["keywords"]),
            post["content"], ",".join(post["hashtags"]), post["fingerprint"],
            datetime.now(timezone.utc).isoformat(), platform
        ))
        self.conn.commit()

    def add_run(self, status, message=""):
        self.conn.execute(
            "INSERT INTO runs(started_at,status,message) VALUES(?,?,?)",
            (datetime.now(timezone.utc).isoformat(), status, message[:2000])
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
