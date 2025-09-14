class Connection:
    def __init__(self, *args, **kwargs):
        pass
    def cursor(self, cursor_factory=None):
        return Cursor()
    def commit(self):
        pass
    def rollback(self):
        pass
    def close(self):
        pass

class Cursor:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    def execute(self, query, params=None):
        # no-op execution stub
        return None
    def fetchall(self):
        return []
    def fetchone(self):
        return None
    def close(self):
        pass

def connect(*args, **kwargs):
    return Connection(*args, **kwargs)

# expose extras submodule providing the RealDictCursor placeholder
from . import extras
