# Plan de pull requests — NkulIA

Huit PR couvrant le backlog de [`docs/ISSUES.md`](ISSUES.md), dans
l'ordre où elles doivent être ouvertes (chaque PR dépend des
précédentes). Titres en [Conventional Commits](../CONVENTIONAL_COMMITS.md).

---

## PR-01 — `chore: bootstrap quality tooling`
**Closes #1, #2**

**Scope** : `pre-commit` (black, ruff, mypy, bandit), `pyproject.toml`
consolidé, `Makefile` (`install`, `lint`, `test`, `run`).
**Hors scope** : CI GitHub Actions (PR-02).
**Validation minimale** : `pre-commit run --all-files` propre sur un clone neuf ; les 4 cibles Makefile fonctionnent.

## PR-02 — `ci: add quality gate and CodeQL`
**Closes #3, #4**

**Scope** : `.github/workflows/ci.yml` (lint + test, matrice Python),
`.github/workflows/codeql.yml`.
**Hors scope** : déploiement (aucun — voir `docs/adr/0001`).
**Validation minimale** : une PR de test avec un lint cassé est bien bloquée par la CI.

## PR-03 — `feat(auth): persist teacher context and local authentication`
**Closes #5, #6**

**Scope** : modèles SQLAlchemy (`Teacher`, `Institution`, `SchoolYear`,
`Subject`, `Classroom`, `TeachingAssignment`, `AuthSession`),
première migration Alembic, hachage Argon2, endpoints
`register`/`login`/`logout`.
**Hors scope** : endpoint profil (PR-04), écrans React (PR-04).
**Validation minimale** : tests unitaires sur mot de passe faux, email dupliqué, session expirée.

## PR-04 — `feat(auth): profile endpoint and screens`
**Closes #7, #8**

**Scope** : `GET/PATCH /me`, écrans React Connexion/Inscription/Profil
(basés sur le prototype HTML déjà validé).
**Hors scope** : changement de mot de passe (ticket futur).
**Validation minimale** : parcours complet testé manuellement dans l'app desktop ; capture d'écran jointe à la PR.

## PR-05 — `feat(import): parse pedagogical DOCX documents`
**Closes #9, #10**

**Scope** : parseur DOCX (`python-docx`), détection des colonnes,
normalisation du schéma de filière (UA/UE ↔ Chapitre/Leçon).
**Hors scope** : interface d'import (PR-06).
**Validation minimale** : les 7 documents du corpus réel s'importent sans erreur ; test de non-régression sur les deux vocabulaires.

## PR-06 — `feat(import): import & analysis screen`
**Closes #11**

**Scope** : écran React (zone de dépôt, liste des documents, statut,
aperçu de hiérarchie).
**Validation minimale** : un import réussi et un import en échec sont tous deux visibles clairement à l'écran.

## PR-07 — `feat(generation): enforce provenance model in generation pipeline`
**Closes #12, #13**

**Scope** : intégration LLM + RAG, contrat de sortie structurée avec
étiquette de provenance obligatoire, premier gabarit de fiche de cours.
**Hors scope** : génération d'évaluations/examens (backlog futur).
**Validation minimale** : test automatisé rejetant toute réponse sans étiquette de provenance ; revue manuelle d'une fiche générée sur le corpus réel.

## PR-08 — `feat(release): PDF export and desktop release workflow`
**Closes #14, #15**

**Scope** : génération PDF (gabarit professionnel), workflow GitHub
Actions de release desktop (PyInstaller → Release GitHub sur tag).
**Validation minimale** : PDF conforme au gabarit du dossier de cadrage ; tag de test produisant une Release avec `.exe` attaché.

---

## Checklist de revue commune à toutes les PR

- [ ] Respecte les principes de `docs/adr/` (offline-first, provenance, `track_schema` neutre)
- [ ] `make lint` et `make test` passent
- [ ] Pas de secret en dur
- [ ] Documentation à jour (`README.md`, `CHANGELOG.md` si applicable)
