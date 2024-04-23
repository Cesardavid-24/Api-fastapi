import peewee
from contextvars import ContextVar
from fastapi import Depends

from app.v1.utils.settings import Settings

settings = Settings()

DB_NAME = settings.db_name
DB_USER = settings.db_user
DB_PASS = settings.db_pass
DB_HOST = settings.db_host
DB_PORT = settings.db_port

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):

    def __init__(self, **kwargs):
        super().__setattr__("__state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getatter__(self,name):
        return self._state.get()[name]
    
db = peewee.MySQLDatabase(DB_NAME,DB_USER,DB_PASS, DB_HOST, DB_PORT)
db._state = PeeweeConnectionState()

async def reset_db_state():
    db._state._state.set(db_state_default.copy())
    db._state.reset()

def get_db(db_state=Depends(reset_db_state)):
    try:
        db.connect()
        yield
    finally:
        if not db.is_closed():
            db.close()
