# M6/M8 companion: a named storage boundary that tests can override.
from fastapi import Request
from m06.database import connect


def get_connection(request: Request):
    with connect(request.app.state.database_path) as connection:
        yield connection
