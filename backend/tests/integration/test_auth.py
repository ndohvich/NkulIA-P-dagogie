"""Tests d'intégration : passent par de vraies requêtes HTTP (TestClient)
contre une vraie base SQLite en mémoire (voir tests/conftest.py) — pas
de mock sur la couche base de données, seule la persistance change
(mémoire au lieu du fichier local)."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.factories import TeacherFactory


def test_register_creates_a_session_token(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "nouveau@exemple.cm",
            "password": "MotDePasse123",
            "last_name": "Yannick",
            "first_name": "Jules",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["teacher"]["email"] == "nouveau@exemple.cm"
    assert "password" not in body["teacher"]
    assert len(body["token"]) > 20


def test_register_rejects_a_duplicate_email(client: TestClient) -> None:
    payload = {
        "email": "duplique@exemple.cm",
        "password": "MotDePasse123",
        "last_name": "Yannick",
        "first_name": "Jules",
    }
    first = client.post("/api/v1/auth/register", json=payload)
    second = client.post("/api/v1/auth/register", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409


def test_register_rejects_a_password_without_a_digit(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "faible@exemple.cm",
            "password": "SansAucunChiffre",
            "last_name": "Yannick",
            "first_name": "Jules",
        },
    )
    assert response.status_code == 422


def test_login_succeeds_with_the_correct_password(client: TestClient, db_session: Session) -> None:
    teacher = TeacherFactory()
    db_session.add(teacher)
    db_session.commit()

    response = client.post(
        "/api/v1/auth/login",
        json={"email": teacher.email, "password": "MotDePasse123"},
    )
    assert response.status_code == 200
    assert response.json()["teacher"]["email"] == teacher.email


def test_login_rejects_a_wrong_password(client: TestClient, db_session: Session) -> None:
    teacher = TeacherFactory()
    db_session.add(teacher)
    db_session.commit()

    response = client.post(
        "/api/v1/auth/login",
        json={"email": teacher.email, "password": "MauvaisMotDePasse1"},
    )
    assert response.status_code == 401


def test_login_rejects_an_unknown_email(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "inconnu@exemple.cm", "password": "MotDePasse123"},
    )
    assert response.status_code == 401


def test_profile_route_requires_authentication(client: TestClient) -> None:
    response = client.get("/api/v1/me")
    assert response.status_code == 401


def test_profile_route_rejects_an_unknown_token(client: TestClient) -> None:
    response = client.get("/api/v1/me", headers={"Authorization": "Bearer jeton-invente"})
    assert response.status_code == 401
