# ADR-0002 : PyWebView plutôt qu'Electron, Tauri ou PySide6

- **Statut** : accepté
- **Date** : 2026-08-19

## Contexte

NkulIA doit avoir l'apparence et la richesse d'un tableau de bord
EdTech moderne (cartes, badges, dégradés, jauges) tout en restant
léger sur des postes d'établissement peu puissants (voir ADR-0001).
Le développement est porté par un seul développeur, dont la
compétence principale est Python, pas Rust ni l'écosystème Node/Electron.

## Décision

Le shell de fenêtre native est **PyWebView**, avec une interface
**React + Vite + Tailwind CSS** affichée dans la fenêtre, et un
backend **FastAPI** exécuté en local par le même processus Python.

## Alternatives considérées

| Option | Avantages | Inconvénients | Retenue ? |
|---|---|---|---|
| Electron + React + backend Python | Écosystème très documenté | Empreinte mémoire élevée (~200-300 Mo au repos) au démarrage, budget lourd sur du matériel bas de gamme | Non |
| Tauri + React + FastAPI | Empreinte très faible, sécurité renforcée | Nécessite Rust, absent des compétences actuelles de l'équipe (une seule personne) ; backend Python en sidecar à assembler | Non (réévaluable plus tard) |
| PySide6 + FastAPI | Tout en Python, widgets natifs légers | Atteindre le rendu visuel « dashboard moderne » attendu prend nettement plus de temps qu'avec une interface web réelle | Non |
| **PyWebView + FastAPI + React** | Tout en Python côté logique métier, interface web réelle pour le rendu visuel, WebView2 déjà préinstallé sur Windows 10/11 | Écosystème PyWebView plus restreint qu'Electron pour les fonctionnalités natives avancées | **Oui** |

## Conséquences

- Toute la logique métier (RAG, génération, parsing) reste en Python,
  ce qui maximise la vitesse d'apprentissage et de contribution pour
  un développeur qui découvre le développement logiciel.
- Le packaging Windows se fait avec PyInstaller (voir le futur workflow
  de release), sans dépendance à un registre d'images ou à Docker.
- Si le projet gagne une équipe frontend/Rust plus tard et que
  l'installeur natif devient un besoin fort, une migration vers Tauri
  reste possible sans changer la logique métier (le frontend React est
  réutilisable presque tel quel).

## Réversibilité

Facile à moyen terme pour la partie frontend (React est découplé du
shell natif). Coûteux à court terme de changer immédiatement de shell,
sans bénéfice mesurable au stade actuel du projet.
