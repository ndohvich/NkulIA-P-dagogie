# Politique de sécurité

## Versions supportées

Le projet est en phase pré-MVP (version `0.x`). Une seule ligne est
maintenue à la fois : la branche `main`.

| Version | Supportée |
| ------- | --------- |
| 0.x     | ✅ |

## Signaler une vulnérabilité

**Ne créez pas d'issue publique pour une faille de sécurité** (mots de
passe, jetons de session, fuite de données enseignant/élève, injection
SQL, etc.).

Envoyez plutôt un message directement au mainteneur :

- GitHub : [@ndohvich](https://github.com/ndohvich)
- Email : `ndohmoise@gmail.com`

Merci d'inclure :
1. Le module concerné (authentification, import de documents, export PDF, etc.)
2. Les étapes pour reproduire le problème
3. L'impact potentiel (accès à quelles données, pour quel utilisateur)

## Délai de réponse visé

Projet solo en développement actif : accusé de réception sous 7 jours,
correction priorisée selon la gravité (`priority: P0` pour toute faille
touchant les mots de passe ou les données personnelles d'un enseignant).

## Périmètre couvert

NkulIA étant une application locale (pas de serveur central), la
surface d'attaque principale est :
- le stockage local des mots de passe (hachage Argon2 — voir `docs/adr/`)
- la validation des fichiers importés (PDF/DOCX potentiellement malveillants)
- les appels sortants vers un fournisseur de LLM (clés API, fuite de contenu pédagogique)
