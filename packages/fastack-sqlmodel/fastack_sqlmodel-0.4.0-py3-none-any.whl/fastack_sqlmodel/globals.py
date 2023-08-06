from fastack.globals import LocalProxy, state

from fastack_sqlmodel import DatabaseState


def _get_db():
    db = getattr(state, "db", None)
    if not isinstance(db, DatabaseState):
        raise RuntimeError("Database not initialized")
    return db


db: DatabaseState = LocalProxy(_get_db)
