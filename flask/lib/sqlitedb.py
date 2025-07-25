import sqlite3
import threading

FETCH_ONE = "fetchone"
FETCH_ALL = "fetchall"


class SQLiteDB:
    def __init__(self):
        self.connection = None
        self.lock = threading.Lock()

    def set_config(self, path=":memory:"):
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row

    def execute(self, query, params=None, fetch=""):
        if not self.connection:
            raise RuntimeError("SQLite DB not initialized")

        with self.lock:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, params or ())
                if fetch == FETCH_ALL:
                    result = cursor.fetchall()
                elif fetch == FETCH_ONE:
                    result = cursor.fetchone()
                else:
                    result = None
                self.connection.commit()
                return result
            except Exception:
                self.connection.rollback()
                raise
            finally:
                cursor.close()


# Shared instance
db = SQLiteDB()
