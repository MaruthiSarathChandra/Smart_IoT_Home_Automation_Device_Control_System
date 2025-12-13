import sqlite3


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from flask import current_app

# Base class for all entity models
Base = declarative_base()

_engine, _SessionLocal = None, None



def _init_engine():
    """Initialize engine and SessionLocal once, using Flask config."""

    global _engine, _SessionLocal

    if _engine is None:
        url = current_app.config['SQLALCHEMY_DATABASE_URI']

        # create engine (equivalent to Hibernate's SessionFactory)
        _engine = create_engine(url, echo=False, future=True)
        _SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)

def get_session():
    """
    Equivalent to getting an EntityManager in JPA.
    Call this inside a request or service when you need DB access.
    """
    if _engine is None:
        _init_engine()

    return _SessionLocal()

def init_db():
    """
    Call this once at app startup (inside app.app_context())
    to create tables based on your models.
    """
    if _engine is None:
        _init_engine()
    Base.metadata.create_all(bind=_engine)



