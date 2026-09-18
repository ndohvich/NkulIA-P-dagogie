# ADR-0001 : Architecture offline-first

- **Statut** : accepté
- **Date** : 2026-08-19

## Contexte

NkulIA est destiné aux enseignants du secondaire camerounais, dans des
établissements où la connexion Internet est souvent instable, parfois
absente en salle informatique. Un enseignant doit pouvoir préparer un
cours, générer une fiche, importer un document et l'exporter en PDF
sans dépendre de la disponibilité du réseau à l'instant T.

## Décision

L'application fonctionne intégralement en local par défaut :
- base de données SQLite embarquée (pas de serveur de base de données) ;
- authentification locale (pas d'identité fédérée en ligne) ;
- génération de documents et export PDF exécutés sur le poste de l'enseignant ;
- seule la génération de contenu par LLM peut nécessiter un accès
  réseau ponctuel — et le système doit rester utilisable (import,
  consultation, export des contenus déjà générés) quand ce réseau est
  indisponible.

## Alternatives considérées

| Option | Avantages | Inconvénients | Retenue ? |
|---|---|---|---|
| Application web classique (SaaS) | Déploiement centralisé, mises à jour simples | Inutilisable sans Internet stable — inadapté au terrain visé | Non |
| Application web + mode hors-ligne (PWA) | Un seul code pour web et offline | Complexité de synchronisation, support offline des navigateurs inégal sur le parc informatique ciblé | Non |
| **Application de bureau locale, sync réseau optionnelle plus tard** | Fonctionne dans les conditions réelles observées sur le terrain | Distribution des mises à jour plus manuelle (exécutable à réinstaller) | **Oui** |

## Conséquences

- Pas de Postgres, Redis, file de tâches (Celery) ou service toujours
  actif : il n'y a pas de serveur à faire tourner en continu à
  superviser — voir ADR-0003 pour le choix de la base de données.
- Le déploiement continu (CD) de ce projet n'est pas un déploiement
  serveur, mais la publication d'un exécutable Windows en Release
  GitHub à chaque tag de version.
- Une synchronisation multi-postes (ex. plusieurs enseignants d'un
  même établissement) est explicitement hors périmètre du MVP ; elle
  ferait l'objet d'un nouvel ADR si elle devient nécessaire.

## Réversibilité

Partiellement réversible : ajouter une synchronisation cloud
optionnelle plus tard est possible sans tout réécrire, tant que le
modèle de données reste local-first dès le départ (pas d'identifiants
générés côté serveur, pas de dépendance implicite à une API distante
dans la couche métier).
