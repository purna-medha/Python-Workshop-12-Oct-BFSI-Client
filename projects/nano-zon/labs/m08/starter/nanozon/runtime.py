# Configuration selects persistence without changing the shopping operations.
import os


def open_store():
    storage_mode = os.getenv("NANOZON_STORAGE", "sqlite")
    if storage_mode == "memory":
        from .memory import MemoryStore
        return MemoryStore()
    if storage_mode != "sqlite":
        raise ValueError("NANOZON_STORAGE must be memory or sqlite")
    from .storage import SQLiteStore
    return SQLiteStore(os.getenv("NANOZON_DATABASE", "data/nanozon.sqlite"))
