# Backlog d'issues — NkulIA

Ce backlog sert de source pour créer les issues GitHub réelles (via
`.github/ISSUE_TEMPLATE/feature_request.yml`). Chaque ligne indique
ses dépendances : ne pas démarrer un ticket dont les dépendances ne
sont pas fermées.

Labels : voir la définition complète dans [`.github/labels.yml`](../.github/labels.yml).

## Épic A — Outillage & qualité

### #1 — Mettre en place pre-commit et consolider `pyproject.toml`
`type: chore` · `priority: P1` · `effort: S` · dépend de : rien

Configurer `black`, `ruff` (remplace isort + flake8), `mypy` et
`bandit` en hooks `pre-commit`. Centraliser toutes les dépendances et
la config des outils dans `backend/pyproject.toml`.
**Terminé lorsque** : `pre-commit run --all-files` passe sans erreur sur le code existant.

### #2 — Créer le `Makefile` de développement
`type: chore` · `priority: P1` · `effort: S` · dépend de : #1

Cibles `make install`, `make lint`, `make test`, `make run`.
**Terminé lorsque** : ces 4 commandes fonctionnent sur un clone neuf.

### #3 — CI GitHub Actions : lint + tests sur chaque PR
`type: chore` · `priority: P0` · `effort: M` · dépend de : #1, #2

Workflow déclenché sur `push` et `pull_request`, matrice Python
3.11/3.12, cache pip.
**Terminé lorsque** : une PR avec une erreur de lint ou un test cassé est bloquée automatiquement.

### #4 — Ajouter l'analyse de sécurité statique (CodeQL)
`type: chore` · `priority: P2` · `effort: S` · dépend de : #3

Workflow CodeQL natif GitHub (pas de compte tiers).
**Terminé lorsque** : l'onglet Security > Code scanning affiche des résultats.

## Épic B — Authentification & profil

### #5 — Modéliser le contexte enseignant + migrations Alembic
`type: feat` · `priority: P0` · `effort: M` · dépend de : #1

Modèles `Teacher`, `Institution`, `SchoolYear`, `Subject`,
`Classroom`, `TeachingAssignment` (voir `docs/ARCHITECTURE.md`).
Première révision Alembic.
**Terminé lorsque** : `alembic upgrade head` crée un schéma propre sur base vide, `alembic downgrade base` le défait proprement.

### #6 — Inscription et connexion locale
`type: feat` · `priority: P0` · `effort: M` · dépend de : #5

Hachage Argon2, jeton de session opaque stocké en base (pas de JWT —
inutile en local). Endpoints `POST /auth/register`, `POST /auth/login`,
`POST /auth/logout`.
**Terminé lorsque** : un email déjà utilisé est refusé, un mauvais mot de passe est refusé, une session expirée est refusée.

### #7 — Endpoint de gestion du profil
`type: feat` · `priority: P1` · `effort: S` · dépend de : #6

`GET /me`, `PATCH /me` (grade, fonction, spécialité, établissement).
**Terminé lorsque** : les champs pré-remplissent un export PDF de test.

### #8 — Écrans React Connexion / Inscription / Profil
`type: feat` · `priority: P1` · `effort: M` · dépend de : #6, #7

Reprendre fidèlement le prototype HTML déjà validé (palette, fil
pédagogique, badges de provenance).
**Terminé lorsque** : le parcours inscription → connexion → profil fonctionne de bout en bout dans l'app desktop.

## Épic C — Import & structuration

### #9 — Parseur DOCX (fiches de progression / projets pédagogiques)
`type: feat` · `priority: P0` · `effort: L` · dépend de : #5

Extraction des tableaux, détection des colonnes (Module, UA/Chapitre,
UE/Leçon, Digitalisation, et colonnes optionnelles du projet pédagogique).
**Terminé lorsque** : les 7 documents du corpus réel (Seconde à Terminale, Niveau 1/2) sont importés sans erreur.

### #10 — Détection automatique du schéma de filière
`type: feat` · `priority: P0` · `effort: M` · dépend de : #9

Reconnaître automatiquement si un document utilise le vocabulaire
« UA/UE » ou « Chapitre/Leçon » et le normaliser vers le modèle
neutre (voir `docs/adr/0003`).
**Terminé lorsque** : les deux vocabulaires produisent la même structure en base.

### #11 — Écran Import & analyse
`type: feat` · `priority: P1` · `effort: M` · dépend de : #9, #10

Zone de dépôt, liste des documents importés, statut d'extraction,
aperçu de la hiérarchie détectée.
**Terminé lorsque** : un enseignant peut importer un fichier et voir le résultat sans lire les logs backend.

## Épic D — Génération pédagogique

### #12 — Modèle de provenance dans le pipeline de génération
`type: feat` · `priority: P0` · `effort: L` · dépend de : #10

Chaque champ généré porte l'une des 4 étiquettes (référence,
déduction, recommandation IA, information manquante) — voir
`docs/adr/` et le principe non négociable du modèle de cadrage.
**Terminé lorsque** : un test automatisé vérifie qu'aucune sortie de génération n'est dépourvue d'étiquette de provenance.

### #13 — Générateur de fiche de cours (premier gabarit)
`type: feat` · `priority: P1` · `effort: L` · dépend de : #12

Génération d'une fiche complète (objectifs, prérequis,
situation-problème, activités) à partir d'une unité sélectionnée.
**Terminé lorsque** : une fiche générée sur une unité du corpus réel est jugée exploitable par l'enseignant (revue manuelle).

## Épic E — Export & publication

### #14 — Export PDF d'une fiche validée
`type: feat` · `priority: P1` · `effort: M` · dépend de : #13

Gabarit PDF professionnel (en-tête établissement, identité visuelle NkulIA).
**Terminé lorsque** : le PDF généré est visuellement conforme au gabarit défini dans le dossier de cadrage.

### #15 — Workflow de release desktop
`type: chore` · `priority: P2` · `effort: M` · dépend de : #2

Sur tag `v*.*.*` : build PyInstaller, publication de l'exécutable en
Release GitHub, changelog généré depuis les commits Conventional
Commits (voir `CONVENTIONAL_COMMITS.md`).
**Terminé lorsque** : un tag de test produit une Release GitHub avec un `.exe` téléchargeable.
