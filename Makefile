.PHONY: install lint format test test-cov run clean precommit migrate
.ONESHELL:
SHELL := /bin/bash

# Installe le backend (mode éditable + dépendances dev) et le frontend.
install:
	python -m venv .venv
	. .venv/bin/activate
	pip install --upgrade pip
	pip install -e "./backend[dev]"
	pre-commit install
	cd frontend && npm install

# Analyse statique : style, typage, sécurité. Zéro modification de fichier.
lint:
	. .venv/bin/activate
	cd backend
	ruff check .
	ruff format --check .
	mypy app
	bandit -q -c pyproject.toml -r app
	cd ../frontend && npm run lint

# Reformate automatiquement (contrairement à `lint`, qui ne fait que vérifier).
format:
	. .venv/bin/activate
	cd backend
	ruff check --fix .
	ruff format .

# Tests backend (couverture ≥ 80 %, voir backend/pyproject.toml) + frontend.
test:
	. .venv/bin/activate
	cd backend && python -m pytest
	cd ../frontend && npm run test

test-cov:
	. .venv/bin/activate
	cd backend && python -m pytest --cov-report=html
	echo "Rapport détaillé : backend/htmlcov/index.html"

# Lance l'application desktop en mode développement (frontend via Vite à part : `cd frontend && npm run dev`).
run:
	. .venv/bin/activate
	python desktop/main.py --dev

# Applique les migrations Alembic sur la base locale (voir backend/migrations/).
migrate:
	. .venv/bin/activate
	cd backend && alembic upgrade head

# Exécute manuellement tous les hooks pre-commit (sans faire de commit).
precommit:
	. .venv/bin/activate
	pre-commit run --all-files

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/.pytest_cache backend/.mypy_cache backend/.ruff_cache backend/htmlcov backend/.coverage
	rm -rf frontend/dist desktop/build desktop/dist
