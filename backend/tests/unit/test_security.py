"""Tests unitaires : aucune base de données, aucun réseau — uniquement
la logique pure de app/core/security.py."""

from app.core.security import generate_session_token, hash_password, verify_password


def test_hash_password_produces_a_different_string_than_the_input() -> None:
    empreinte = hash_password("MotDePasse123")
    assert empreinte != "MotDePasse123"


def test_verify_password_accepts_the_correct_password() -> None:
    empreinte = hash_password("MotDePasse123")
    assert verify_password("MotDePasse123", empreinte) is True


def test_verify_password_rejects_a_wrong_password() -> None:
    empreinte = hash_password("MotDePasse123")
    assert verify_password("UnAutreMotDePasse", empreinte) is False


def test_verify_password_never_raises_on_garbage_hash() -> None:
    """Un empreinte corrompue (ex. donnée invalide en base) doit renvoyer
    False, jamais faire planter la route de connexion."""
    assert verify_password("peu importe", "ceci-n-est-pas-une-empreinte-argon2") is False


def test_generate_session_token_produces_unique_values() -> None:
    premier = generate_session_token()
    second = generate_session_token()
    assert premier != second
    assert len(premier) > 20
