"""Dépendances FastAPI partagées entre les routes protégées.

Une "dépendance" FastAPI est une fonction que `Depends(...)` exécute
avant votre route : pratique pour factoriser une vérification (ici,
"cette requête a-t-elle une session valide ?") sans la copier-coller
dans chaque route qui en a besoin.
"""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import AuthSession, Teacher
from app.db.session import get_db


def get_current_teacher(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> Teacher:
    """Vérifie l'en-tête `Authorization: Bearer <jeton>` et renvoie
    l'enseignant correspondant, ou refuse la requête (401).

    On lève systématiquement la même erreur générique, que le jeton
    soit absent, inconnu ou expiré : donner un message différent selon
    le cas aiderait un attaquant à deviner quels jetons existent.
    """
    erreur_non_autorise = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentification requise ou expirée.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not authorization or not authorization.startswith("Bearer "):
        raise erreur_non_autorise

    token = authorization.removeprefix("Bearer ").strip()
    session = db.query(AuthSession).filter(AuthSession.token == token).first()

    if session is None:
        raise erreur_non_autorise

    expires_at = session.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=UTC)
    if expires_at < datetime.now(UTC):
        raise erreur_non_autorise

    return session.teacher
