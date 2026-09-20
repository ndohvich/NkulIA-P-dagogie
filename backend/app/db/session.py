"""Connexion à la base SQLite locale.

Un `Engine` SQLAlchemy représente la base de données ; une `Session`
représente une conversation avec elle (le temps d'une requête HTTP).
On crée un engine une seule fois au démarrage, et une session neuve
à chaque requête — c'est le rôle de `get_db` ci-dessous.
"""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

# check_same_thread=False est nécessaire car FastAPI peut servir une
# requête sur un thread différent de celui qui a ouvert la connexion ;
# SQLite l'autorise tant qu'une seule requête à la fois écrit — ce qui
# correspond à notre usage mono-utilisateur local.
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Classe de base dont hériteront tous les modèles (voir models.py)."""


def get_db() -> Generator[Session, None, None]:
    """Fournit une session de base de données à une route FastAPI, puis la ferme.

    FastAPI appelle cette fonction pour chaque requête grâce à `Depends(get_db)` ;
    le `yield` renvoie la session pendant la requête, et le code après le
    `yield` s'exécute automatiquement une fois la réponse envoyée — c'est
    ce qui garantit que la session est toujours fermée, même en cas d'erreur.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
