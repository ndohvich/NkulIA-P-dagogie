# Conventional Commits — référence NkulIA

Ce projet suit [Conventional Commits 1.0.0](https://www.conventionalcommits.org/fr/v1.0.0/).
Chaque message de commit a la forme :

```
<type>(<portée optionnelle>): <description au présent, en minuscule>

[corps optionnel]

[pied optionnel : Closes #12, BREAKING CHANGE: ...]
```

## Types utilisés dans ce projet

| Type | Usage | Exemple |
|---|---|---|
| `feat` | Nouvelle fonctionnalité visible | `feat(auth): ajoute l'inscription enseignant` |
| `fix` | Correction de bug | `fix(import): gère les fichiers .docx sans tableau` |
| `docs` | Documentation uniquement | `docs(adr): documente le choix PyWebView` |
| `chore` | Outillage, dépendances, config | `chore(deps): met à jour fastapi vers 0.116` |
| `refactor` | Changement interne, sans effet visible | `refactor(db): extrait la session dans un module dédié` |
| `test` | Ajout ou correction de tests | `test(auth): ajoute les cas de mot de passe invalide` |
| `perf` | Amélioration de performance | `perf(rag): met en cache les embeddings d'un document` |
| `ci` | Workflows GitHub Actions | `ci: ajoute le job CodeQL` |

## Portées (scope) courantes

`auth`, `import`, `rag`, `generation`, `pdf`, `desktop`, `db`, `ci`, `adr`.

## Rupture de compatibilité

Un commit qui casse la compatibilité (ex. migration de schéma non
rétrocompatible) ajoute `BREAKING CHANGE:` dans le pied de commit, et
déclenche une montée de version MAJEURE selon Semantic Versioning.

## Pourquoi cette convention ici

Deux bénéfices concrets, pas seulement esthétiques :
1. Le `CHANGELOG.md` peut être reconstruit automatiquement à partir de
   l'historique Git plutôt que rédigé à la main.
2. Le type de commit indique directement le niveau de version SemVer
   à incrémenter (`fix` → PATCH, `feat` → MINOR, `BREAKING CHANGE` → MAJOR).
