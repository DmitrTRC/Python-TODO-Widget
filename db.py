import sqlite3
import os
from PySide6.QtCore import QStandardPaths
from logger import logger

class TodoDAO:
    def __init__(self):
        # Determine the correct AppData location
        app_data_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        # Ensure we place it in a TodoWidget specific directory
        self.db_dir = os.path.join(app_data_dir, "TodoWidget")
        os.makedirs(self.db_dir, exist_ok=True)
        
        self.db_path = os.path.join(self.db_dir, "todos.db")
        logger.debug(f"Database path initialized at: {self.db_path}")
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS todos (
                    id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    completed INTEGER DEFAULT 0,
                    created_at INTEGER
                )
            ''')
            conn.commit()

    def get_todos(self):
        """Returns a list of all todos ordered by creation time."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, text, completed, created_at FROM todos ORDER BY created_at ASC')
            rows = cursor.fetchall()
            return [{'id': row[0], 'text': row[1], 'completed': bool(row[2]), 'created_at': row[3]} for row in rows]

    def add_todo(self, todo_id: str, text: str, created_at: int):
        """Inserts a new todo item."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO todos (id, text, completed, created_at) VALUES (?, ?, 0, ?)',
                (todo_id, text, created_at)
            )
            conn.commit()

    def update_todo(self, todo_id: str, text: str = None, completed: bool = None):
        """Updates an existing todo item's text or completed status."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if text is not None and completed is not None:
                cursor.execute('UPDATE todos SET text = ?, completed = ? WHERE id = ?', (text, int(completed), todo_id))
            elif text is not None:
                cursor.execute('UPDATE todos SET text = ? WHERE id = ?', (text, todo_id))
            elif completed is not None:
                cursor.execute('UPDATE todos SET completed = ? WHERE id = ?', (int(completed), todo_id))
            conn.commit()

    def delete_todo(self, todo_id: str):
        """Deletes a todo item."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
            conn.commit()
