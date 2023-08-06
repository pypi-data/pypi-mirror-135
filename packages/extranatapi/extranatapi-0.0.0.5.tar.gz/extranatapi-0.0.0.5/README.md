# Extranat API

Extranat API permet

* d'accèder aux données publique de l'Extranat de la FFN
* de calculer les points pour les nageurs (option pour les masters)
* de recherche la meilleur équipe pour une compétition

Il est nécessaire d'avoir [python](https://www.python.org/). *Lors de l'installation de python sous Windows, cocher l'option `Add Python xx to PATH`.*

## Usage

Installation

```bash
pip install extranatapi
```

Désinstallation

```bash
pip uninstall extranatapi
```

Commandes

Sous linux ou Windows

```bash
extranat-cli [parameters]
```

Sortie `--format`

* json
* column
* csv
* text

Le séparateur pour CSV doit être `;`.

### Liste des régions

```bash
extranat-cli --list-regions
extranat-cli --list-regions --format=json
extranat-cli --list-regions --format=column
extranat-cli --list-regions --format=csv
extranat-cli --list-regions --format=text
```

### Liste des départements

```bash
extranat-cli --list-departements
extranat-cli --list-departements --format=json
extranat-cli --list-departements --format=column
extranat-cli --list-departements --format=csv
extranat-cli --list-departements --format=text
```

### Liste des clubs

```bash
extranat-cli --list-clubs
extranat-cli --list-clubs --format=json
extranat-cli --list-clubs --format=column
extranat-cli --list-clubs --format=csv
extranat-cli --list-clubs --format=text
```

### Liste des nages

```bash
extranat-cli --list-nages
extranat-cli --list-nages --format=json
extranat-cli --list-nages --format=column
extranat-cli --list-nages --format=csv
extranat-cli --list-nages --format=text
```

### Saison d'un club

Affiche les résultats des compétitions d'une saison pour un club.

```bash
extranat-cli --saison --annee=xx --idclub=xx
extranat-cli --saison --annee=xx --idclub=xx --format=json
extranat-cli --saison --annee=xx --idclub=xx --format=column
extranat-cli --saison --annee=xx --idclub=xx --format=csv
extranat-cli --saison --annee=xx --idclub=xx --format=text
```

### Nageur

Affiche les résultats d'un nageur (Meilleures performances ou toutes avec --all)

```bash
extranat-cli --nageur <iuf>
extranat-cli --nageur <iuf> --all

extranat-cli --nageur <fichier_csv_or_xlsx>
extranat-cli --nageur <fichier_csv_or_xlsx> --all
extranat-cli --nageur <fichier_csv_or_xlsx> --format=csv
extranat-cli --nageur <fichier_csv_or_xlsx> --format=csv  --file=<cvs_file>
extranat-cli --nageur <fichier_csv_or_xlsx> --format=xlsx --file=<excel_file>
```

Le fichier `fichier_csv_or_xlsx` doit contenir le champ `iuf`.

### Cotation

Calcul les points pour chaque nage du fichier CSV/EXCEL.

Le fichier `fichier_csv_or_xlsx` doit contenir les champs: `nageur`, `annee`, `age`, `iuf`, `sexe`, `bassin`, `nage`, `temps`.

```bash

# cotation
extranat-cli --cotation <fichier_csv_or_xlsx> --format=csv
extranat-cli --cotation <fichier_csv_or_xlsx> --format=csv  --file=<cvs_file>
extranat-cli --cotation <fichier_csv_or_xlsx> --format=xlsx --file=<excel_file>

# cotation pour les MASTERS (avec coefficient)
extranat-cli --cotation <fichier_csv_or_xlsx> --master --format=csv
extranat-cli --cotation <fichier_csv_or_xlsx> --master --format=csv  --file=<cvs_file>
extranat-cli --cotation <fichier_csv_or_xlsx> --master --format=xlsx --file=<excel_file>
```

### Recherche d'une équipe

Recherche de la meilleur équipe pour une compétition donnée.

Le fichier `fichier_NAGES_csv_or_xlsx` représente la liste des nages à nager. Il doit contenir le champ `nage`.

Le fichier `fichier_NAGEURS_csv_or_xlsx` représente la liste des nageurs à utiliser pour déterminer l'équipe.
Il doit contenir les champs `nageur`, `annee`, `age`, `iuf`, `sexe`, `bassin`, `nage`, `temps`, `points`

```bash
# Recherche d'une équipe
extranat-cli --recherche_equipe <fichier_NAGES_csv_or_xlsx> <fichier_NAGEURS_csv_or_xlsx>

# Recherche d'une équipe Masculine
extranat-cli --recherche_equipe <fichier_NAGES_csv_or_xlsx> <fichier_NAGEURS_csv_or_xlsx> M

# Recherche d'une équipe Féminine
extranat-cli --recherche_equipe <fichier_NAGES_csv_or_xlsx> <fichier_NAGEURS_csv_or_xlsx> F

# Recherche d'une équipe avec <N> Dames ou Messieurs
extranat-cli --recherche_equipe <fichier_NAGES_csv_or_xlsx> <fichier_NAGEURS_csv_or_xlsx> <N>
extranat-cli --recherche_equipe <fichier_NAGES_csv_or_xlsx> <fichier_NAGEURS_csv_or_xlsx> 1
```

## Cas d'usage

### Génération d'un fichier nageur/nage/cotation

Etapes

* Extraire d'Extranat la liste des membres du club

* Récupération des temps des nageurs

```bash
extranat-cli --nageur ffn_extraction_CLUB_ANNEE.xlsx --format=xlsx --file=nageurs_temps.xlsx
```

* Modifier le fichier `nageurs_temps.xlsx` pour ajouter/modifier/supprimer des nageurs/nages/temps.

* Calcul des points de cotation

```bash
# Compétitions jeunes
extranat-cli --cotation nageurs_temps.xlsx --format=xlsx --file=nageurs_cotation.xlsx

# Compétitions master
extranat-cli --cotation nageurs_temps.xlsx --format=xlsx --file=nageurs_cotation.xlsx --master
```

### Génération d'une équipe

* Faire les étapes **Génération d'un fichier nageur/nage/cotation**

* Créer un fichier Excel `nages.xlsx` avec la liste des nages. La première cellule doit être `nage`.

Pour avoir le nom des nages:

```bash
# Liste des nages
extranat-cli --list-nages
```

* Recherche d'une équipe

```bash
# Recherche d'une équipe avec <N> Dames ou Messieurs
extranat-cli --recherche_equipe nages.xlsx nageurs_cotation.xlsx <N>
```
