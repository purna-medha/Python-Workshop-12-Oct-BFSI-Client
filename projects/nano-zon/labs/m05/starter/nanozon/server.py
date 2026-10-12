# The server entry point initializes its configured storage when explicitly launched.
from .api import create_app
from .runtime import open_store

app = create_app(open_store())
# Launch: uv run uvicorn nanozon.server:app --port 8000
