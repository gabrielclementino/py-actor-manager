import sqlite3
from app.models import Actor


class ActorManager:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS actors (
                id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def create(self, actor: Actor):
        self.cursor.execute(
            "INSERT INTO actors (id, first_name, last_name) VALUES (?, ?, ?)",
            (actor.id, actor.first_name, actor.last_name)
        )
        self.conn.commit()

    def get(self, actor_id: int) -> Actor:
        self.cursor.execute("SELECT * FROM actors WHERE id = ?", (actor_id,))
        row = self.cursor.fetchone()
        return Actor(*row) if row else None

    def update(self, actor: Actor):
        self.cursor.execute(
            "UPDATE actors SET first_name = ?, last_name = ? WHERE id = ?",
            (actor.first_name, actor.last_name, actor.id)
        )
        self.conn.commit()

    def delete(self, actor_id: int):
        self.cursor.execute("DELETE FROM actors WHERE id = ?", (actor_id,))
        self.conn.commit()
