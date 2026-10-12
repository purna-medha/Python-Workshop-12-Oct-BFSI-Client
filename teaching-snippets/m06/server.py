# Optional M6 companion: run the persistent API without changing lesson snippets.
# Importing this server entry point intentionally initializes the chosen database.
import os
from m06.api import create_app
from m06.database import connect, initialize

database_path = os.getenv("NANOZON_DATABASE", "teaching-shop.sqlite")
with connect(database_path) as connection:
    initialize(connection)
app = create_app(database_path)
# Launch: uv run uvicorn m06.server:app --port 8000
