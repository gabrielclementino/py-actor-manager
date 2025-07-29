import sqlite3
from app.models import Actor


class ActorManager:
    def __init__(self, db_name: str, table_name: str):
        self.db_name = db_name
        self.table_name = table_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def create(self, actor: Actor):
        self.cursor.execute(
            f"INSERT INTO {self.table_name} (id, first_name, last_name) VALUES (?, ?, ?)",
            (actor.id, actor.first_name, actor.last_name)
        )
        self.conn.commit()

    def get(self, actor_id: int) -> Actor:
        self.cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE id = ?",
            (actor_id,)
        )
        row = self.cursor.fetchone()
        return Actor(*row) if row else None

    def update(self, actor: Actor):
        self.cursor.execute(
            f"UPDATE {self.table_name} SET first_name = ?, last_name = ? WHERE id = ?",
            (actor.first_name, actor.last_name, actor.id)
        )
        self.conn.commit()

    def delete(self, actor_id: int):
        self.cursor.execute(
            f"DELETE FROM {self.table_name} WHERE id = ?",
            (actor_id,)
        )
        self.conn.commit()
