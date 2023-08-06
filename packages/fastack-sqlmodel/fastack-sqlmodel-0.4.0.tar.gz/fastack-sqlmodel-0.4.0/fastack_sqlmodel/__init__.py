import os

from fastack import Fastack
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import close_all_sessions
from sqlmodel import SQLModel, create_engine

from fastack_sqlmodel.session import Session


class DatabaseState:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.sessionmaker = sessionmaker(class_=Session)

    def open(self, engine: Engine = None, **kwds) -> Session:
        engine = engine or self.engine
        session = self.sessionmaker(bind=engine, **kwds)
        return session


def setup(app: Fastack):
    def on_startup():
        uri = getattr(app.state.settings, "SQLALCHEMY_DATABASE_URI", None)
        if not uri:
            raise RuntimeError("SQLALCHEMY_DATABASE_URI is not set")

        options = getattr(app.state.settings, "SQLALCHEMY_OPTIONS", {})
        engine = create_engine(uri, **options)
        app.state.db = DatabaseState(engine)
        SQLModel.metadata.create_all(engine)

    def on_shutdown():
        # FIXME: Currently I have no idea for this, the code below aims to ignore closing all database connections.
        # This is because I'm currently building a plugin for integration with APScheduler
        # and getting issues due to the code below :(
        if "SQLALCHEMY_IGNORE_CLOSE_SESSION" in os.environ:
            return

        close_all_sessions()

    app.add_event_handler("startup", on_startup)
    app.add_event_handler("shutdown", on_shutdown)
