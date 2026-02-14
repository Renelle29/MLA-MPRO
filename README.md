### Modèles de Localisations Avancés

**Thierry Zheng & Ronan Le Prat**

Ce dépôt contient des implémentations & heuristiques pour des problèmes de localisations.

### Data

Les fichiers de données sont nommés de la manière suivante: 

`{Nombre de clients}_{Nombre de sites}_{Côté de la grille}_{Seed}`

Pour charger une instance, appeler la fonction `load_instance_json(filename)`.

Cela retourne un dictionnaire contenant les clés suivantes:

- `n`: Nombre de clients
- `m`: Nombre de sites
- `coordinates_n`: Coordonnées des clients dans la grille
- `coordinates_m`: Coordonnées des sites dans la grille
- `f`: Coûts fixes d'ouverture de site
- `meta`: Meta-données - Côté le la grille `L` - Seed `seed`

La fonction `distance` renvoie la distance de Manhattan (norme 1) entre deux points de la grille (donnés sous forme de liste).