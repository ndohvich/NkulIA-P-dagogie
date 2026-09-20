"""Sécurité locale : mots de passe et sessions.

Règle non négociable (voir docs/ARCHITECTURE.md et CONTRIBUTING.md) :
un mot de passe n'est JAMAIS stocké en clair. On stocke uniquement son
empreinte Argon2 — une fonction à sens unique : facile à vérifier,
impossible à inverser pour retrouver le mot de passe d'origine.
"""

from __future__ import annotations

import secrets
from datetime import UTC, datetime, timedelta

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

from app.core.config import get_settings

# PasswordHasher() utilise les paramètres Argon2id recommandés par défaut
# (mémoire, itérations, parallélisme) — inutile de les régler à la main
# tant que le profil de performance du poste enseignant n'est pas mesuré.
_hasher = PasswordHasher()


def hash_password(plain_password: str) -> str:
    """Transforme un mot de passe en clair en une empreinte sûre à stocker."""
    return _hasher.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Vérifie qu'un mot de passe correspond à une empreinte stockée.

    Ne lève jamais d'exception vers l'appelant : un mot de passe qui ne
    correspond pas (`VerificationError`, dont `VerifyMismatchError`) ou
    une empreinte corrompue/mal formée en base (`InvalidHashError`,
    trouvé par le test `test_verify_password_never_raises_on_garbage_hash`)
    sont tous les deux traités comme « faux », pas comme une erreur.
    """
    try:
        _hasher.verify(password_hash, plain_password)
        return True
    except (VerificationError, InvalidHashError):
        return False


def generate_session_token() -> str:
    """Crée un jeton de session aléatoire, impossible à deviner.

    secrets.token_urlsafe est fait pour ça : il utilise un générateur
    aléatoire cryptographiquement sûr (contrairement au module `random`,
    qui ne doit jamais servir à produire un secret).
    """
    return secrets.token_urlsafe(32)


def session_expiry() -> datetime:
    """Calcule la date d'expiration d'une nouvelle session."""
    settings = get_settings()
    return datetime.now(UTC) + timedelta(hours=settings.session_ttl_hours)
