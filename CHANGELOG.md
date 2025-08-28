# Changelog

Toutes les modifications notables de ce projet seront documentées ici.  
Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/).

---

## [v1.0.0] - 2025-08-27
### Ajouté
- Version initiale du scraper 🎉
- Recherche simple par URL.
- Ajout du fichier `requirements.txt`.
- Ajout d’une première description du projet.

---

## [v1.1.0] - 2025-08-28
### Ajouté
- Sélection de la langue des offres (FR 🇫🇷, EN 🇬🇧, DE 🇩🇪).
- Vérification des URLs via regex (pas de filtres autorisés).
- Fonction de chargement automatique de toutes les offres.
- Extraction de la qualité des cartes affichée avec le prix.
- Section **statistiques** :  
  - Moyenne simple  
  - Prix le plus fréquent  
  - Prix conseillé via méthode IQR (hors extrêmes)
- Refactoring : code réorganisé par sections.

---