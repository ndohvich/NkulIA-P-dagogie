"""Configuration pytest partagée par les trois couches de tests.

Principe clé : chaque test tourne contre une base SQLite **en mémoire**,
créée et détruite pour ce test précis — jamais contre la vraie base de
développement. `StaticPool` force SQLAlchemy à garder une seule
connexion ouverte (une base ':memory:' normale disparaîtrait entre deux
connexions, ce qu'on ne veut pas pendant un test).
"""

from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base, get_db
from app.main import app


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Un TestClient dont la dépendance get_db pointe vers la base de
    test isolée ci-dessus, au lieu de la vraie base SQLite locale."""

    def _override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
