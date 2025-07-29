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

    def create(self, first_name: str, last_name: str):
        self.cursor.execute(
            f"INSERT INTO {self.table_name} "
            f"(first_name, last_name) VALUES (?, ?)",
            (first_name, last_name)
        )
        self.conn.commit()

    def all(self) -> list[Actor]:
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        rows = self.cursor.fetchall()
        return [Actor(*row) for row in rows]

    def get(self, actor_id: int) -> Actor:
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        self.cursor.execute(query, (actor_id,))
        row = self.cursor.fetchone()
        return Actor(*row) if row else None

    def update(self, actor: Actor):
        query = (
            f"UPDATE {self.table_name} "
            f"SET first_name = ?, last_name = ? "
            f"WHERE id = ?"
        )
        params = (actor.first_name, actor.last_name, actor.id)
        self.cursor.execute(query, params)
        self.conn.commit()

    def delete(self, actor_id: int):
        self.cursor.execute(
            f"DELETE FROM {self.table_name} WHERE id = ?",
            (actor_id,)
        )
        self.conn.commit()
