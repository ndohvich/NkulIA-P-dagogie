# ADR-0003 : SQLite local plutôt que Postgres + Redis

- **Statut** : accepté
- **Date** : 2026-08-19

## Contexte

Une architecture web classique associerait souvent une base
relationnelle serveur (Postgres) et un cache/file de tâches (Redis,
Celery) pour absorber la charge de plusieurs utilisateurs concurrents.
NkulIA est utilisé par **un seul enseignant, sur son propre poste**
(voir ADR-0001) : il n'y a pas de charge concurrente à absorber, ni de
tâche de fond partagée entre plusieurs utilisateurs à mettre en file.

## Décision

Toutes les données (contexte enseignant, progressions, contenus
générés, historique) sont stockées dans un **fichier SQLite local**,
géré via SQLAlchemy et versionné avec Alembic. Aucun serveur de base
de données, aucun cache distribué, aucune file de tâches.

## Alternatives considérées

| Option | Avantages | Inconvénients | Retenue ? |
|---|---|---|---|
| Postgres | Robuste, standard en production web | Nécessite un service actif à installer/superviser sur un poste enseignant — contraire à ADR-0001 | Non |
| Postgres + Redis + Celery | Adapté à un vrai service multi-utilisateurs | Aucun des problèmes du MVP ne nécessite du multi-utilisateurs concurrent ni des tâches de fond partagées ; complexité et surface de bugs non justifiées pour un seul développeur | Non |
| **SQLite + SQLAlchemy + Alembic** | Zéro service à installer, fichier unique sauvegardable, largement suffisant pour un usage mono-utilisateur | Moins adapté si le projet évolue un jour vers un vrai multi-utilisateurs concurrent en ligne | **Oui** |

## Conséquences

- Les migrations de schéma (Alembic) doivent rester compatibles avec
  SQLite (types limités, `ALTER TABLE` plus contraint que sur Postgres).
- Une tâche longue (ex. génération RAG) s'exécute en tâche de fond
  **dans le même processus** (via les tâches asynchrones de FastAPI),
  sans file de messages externe.
- Si un jour une synchronisation multi-postes est ajoutée, ce sera
  l'objet d'un nouvel ADR — probablement une synchronisation
  fichier-à-fichier ou via une API distante optionnelle, pas une
  migration complète vers Postgres.

## Réversibilité

Moyennement coûteux : SQLAlchemy abstrait une partie du dialecte SQL,
mais une migration vers Postgres nécessiterait de revalider les
migrations Alembic et certains types de colonnes. Ce coût est jugé
acceptable **si et seulement si** un besoin multi-utilisateurs réel
apparaît — ce qui n'est pas le cas du MVP.
