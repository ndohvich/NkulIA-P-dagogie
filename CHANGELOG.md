# Changelog

Toutes les modifications notables de ce projet sont documentées ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et le projet adhère à [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### Ajouté
- Gouvernance GitHub complète : modèles d'issues, modèle de PR, `CODEOWNERS`, labels centralisés (`.github/labels.yml`), étiquetage automatique des PR par domaine
- Documentation communautaire : `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`, `CONVENTIONAL_COMMITS.md`
- Trois premières décisions d'architecture documentées (`docs/adr/0001` à `0003`) : offline-first, PyWebView, SQLite
- Backlog initial de 15 issues et plan de 8 pull requests (`docs/ISSUES.md`, `docs/PULL_REQUESTS.md`)
- Squelette applicatif : backend FastAPI, frontend React/Vite/Tailwind, lanceur desktop PyWebView
- Authentification locale complète (issues #5–#8) : modèles SQLAlchemy, migration Alembic initiale, hachage Argon2, endpoints `register`/`login`/`logout`/`me`, 14 tests (unit/integration/e2e), 97 % de couverture
- Outillage qualité : `pre-commit` (ruff, mypy, bandit, gitleaks), `pyproject.toml` consolidé, `Makefile`
- CI GitHub Actions (`ci.yml`), analyse de sécurité statique (`codeql.yml`), workflow de release desktop (`release.yml`)
- Import de documents pédagogiques (issues #9-#10) : parseur DOCX (fiches de progression et projets pédagogiques), détection automatique du vocabulaire de filière (UA/UE vs Chapitre/Leçon) depuis l'en-tête, modèle de données Module → Unité intermédiaire → Unité fine, endpoints `POST /ingestion/import`, `GET /ingestion/documents`, `GET /ingestion/documents/{id}/warnings` — 22 nouveaux tests contre le corpus réel (35 au total), 97,6 % de couverture

### En attente de décision
- Licence du projet — voir `README.md`, section Licence

## [0.0.0] - 2026-09-18
### Ajouté
- Initialisation du dépôt
