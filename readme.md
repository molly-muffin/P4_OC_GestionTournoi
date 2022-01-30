# Application de gestion de tournoi 

## Contexte du projet : 
Une association m'a contactée afin de créer une application de gestion de tournoi en local permettnt ainsi d'éviter les problèmes de connexion.

## But du projet : 
Gérer un tournoi d'échec avec le système de tournoi Suisse. Les matchs doivent se faire en 2 joueurs de même niveau et ne doivent pas se répéter entre 2 mêmes joueurs.

### Statut du projet : 
| Etapes | Avancement |
| ------ | ------ |
| Définir (et coder) les modèles pour ce projet | **Terminé** |
| Mettre en œuvre la conception MVC | **Terminé** |
| Implémenter la sérialisation | **Terminé** |
| Documenter l'application | **Terminé** |
| Rapport flake8 | **Terminé** |

### Le script permet :
*	Créer des joueurs et les sauvegarder dans un fichier `json`
*	Mettre à jour le classement des joueurs et le sauvegarder
*	Créer des tournois et les sauvegarder dans un fichier `json`
*	Arrêter un torunoi, le sauverager et pouvoir le reprendre plus tard

### Environnement de développement : 
`Python 3.9.5`

### Méthode utilisée : 
L'application est codé selon le design pattern `Modèle-Vue-Contrôleur (MVC)` avec une sauvegarde des joueurs et des tournois grâce à TinyDB.

### Instruction d’installation et d’utilisation :
Les différents réperetoires doivent être télécharger dans un dossier.
*	Prérequis
	L'application requière l'utilisation de différentes librairies lister dans le fichier `requirements.txt`
	Dans un terminal installer un environnement externe avec la commande :
	```bash
	pip install venv
	```
	Puis installer les librairies requises avec la commande :
	```bash
	pip install -r requirement.txt
	```
*	Lancement 
	Dans un terminal lancer l'applicaton dans le dossier de téléchargement du script avec la commande :
	```bash
	python main.py
	``` 
## Ce que j'ai appris :
Je me suis familiarisé avec les classes et la programmation orientée objet qui permet de structurer un programme en regroupant des propriétés et des comportements associés dans des objets individuels.
J'ai également appris à structurer mon code grâce au modèle `MVC` (Models, Views, Controllers).
Et enfin j'ai pu apprendre la sérialisation de données grâce à TinyDB.

> Laureenda Demeule
> OpenClassroom 