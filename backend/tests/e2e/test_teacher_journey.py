"""Test end-to-end : rejoue le parcours « Premier lancement » décrit
dans docs/CAHIER_DE_REALISATION.md — inscription, consultation du
profil, mise à jour, déconnexion, puis refus de l'ancien jeton.

Un seul scénario, de bout en bout, plutôt que des cas isolés : c'est le
rôle de la couche e2e (les cas particuliers sont déjà couverts par les
tests d'intégration)."""

from fastapi.testclient import TestClient


def test_full_teacher_journey_register_profile_logout(client: TestClient) -> None:
    # 1. Inscription (voir docs/ISSUES.md #6)
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "parcours@exemple.cm",
            "password": "MotDePasse123",
            "last_name": "Yannick",
            "first_name": "Jules",
            "institution_name": "Lycée Technique d'Ébolowa",
            "subject_taught": "Informatique",
        },
    )
    assert register_response.status_code == 201
    token = register_response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Consultation du profil (voir docs/ISSUES.md #7)
    profile_response = client.get("/api/v1/me", headers=headers)
    assert profile_response.status_code == 200
    assert profile_response.json()["institution_name"] == "Lycée Technique d'Ébolowa"

    # 3. Mise à jour du profil — un enseignant complète son grade et sa spécialité
    update_response = client.patch(
        "/api/v1/me",
        headers=headers,
        json={"grade": "PLEG", "specialty": "Génie logiciel"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["grade"] == "PLEG"
    # Un champ non envoyé (ex. subject_taught) ne doit pas être écrasé :
    assert update_response.json()["subject_taught"] == "Informatique"

    # 4. Déconnexion
    logout_response = client.post("/api/v1/auth/logout", headers=headers)
    assert logout_response.status_code == 204

    # 5. L'ancien jeton ne doit plus jamais fonctionner
    after_logout_response = client.get("/api/v1/me", headers=headers)
    assert after_logout_response.status_code == 401
