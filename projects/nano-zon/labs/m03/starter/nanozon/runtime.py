# Supplied checkpoint storage; SQLite arrives in M6.
from .memory import MemoryStore


def open_store():
    return MemoryStore()
