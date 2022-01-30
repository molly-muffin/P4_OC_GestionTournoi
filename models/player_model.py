#############
#  LIBRARY  #
#############
from tinydb import TinyDB
import time

############
#  SCRIPT  #
############
from views import main_view
from controllers import main_controller

###############
#  VARIABLES  #
###############
player_db = TinyDB('models/players.json')

######################
#  CLASS & FUNCTION  #
######################
class Player(object):
	"""Instancier un joueur"""
	#méthode init
	def __init__(self, 
				name=None, 
				first_name=None, 
				birthday=None, 
				sexe=None, 
				ranking=None, 
				tournament_score=0,
				player_id=0):
		#attributs
		self.name = name
		self.first_name = first_name
		self.birthday = birthday
		self.sexe = sexe
		self.ranking = ranking	
		self.tournament_score = tournament_score
		self.player_id = player_id

	#sérialisation  
	def serialized(self):
		player_details = {}
		player_details['Nom'] = self.name
		player_details['Prenom'] = self.first_name
		player_details['Anniversaire'] = self.birthday
		player_details['Sexe'] = self.sexe
		player_details['Classement'] = self.ranking
		player_details['Score'] = self.tournament_score
		player_details['ID du joueur'] = self.player_id
		return player_details			

	#désérialisation  
	def unserialized(self, serialized_player):
		name = serialized_player['Nom']
		first_name = serialized_player['Prenom']
		birthday = serialized_player['Anniversaire']
		sexe = serialized_player['Sexe']
		ranking = serialized_player['Classement']
		tournament_score = serialized_player['Score']
		player_id = serialized_player['ID du joueur']
		return Player(name,
					first_name,
					birthday,
					sexe,
					ranking,
					tournament_score,
					player_id
					)
	#méthode str --> retourne le nom et le prénom du joueur
	def __str__(self):
		return f"{self.name} {self.first_name}"

	#méthode repr --> retourne le nom, prénom et classement du joueur
	def __repr__(self):
		return f"{self.name} {self.first_name}, classement : {self.ranking}"

	#Mettre à jour le classement d'un joueur
	def update_ranking(self):
		self.main_menu = main_controller.MainMenu()
		self.view_players = main_view.PlayersDiplay()
		self.players_db = player_db
		self.view_players()

		valid_id = False
		#Choisir un  joueur
		while not valid_id:
			player_id = input("Ecrire le numéro du joueur : \n --> ")
			if player_id.isdigit() and int(player_id) >= 0 and int(player_id) <= len(self.players_db):
				valid_id = True
			else:
				print("Vous devez écrire un numéro correspondant à un joueur.")

		valid_ranking = False
		#Nouveau classement du  joueur
		while not valid_ranking:
			new_ranking = input("Ecrire le nouveau classement : \n --> ")
			if new_ranking.isdigit() and int(new_ranking) >= 0:
				valid_ranking = True
			else:
				print("Vous devez écrire un nombre entier positif.")

		player_to_modify = player_db.get(doc_id=int(player_id))
		player_to_modify['Classement'] = new_ranking
		#Montrer l'update du joueur
		print(
			f"{player_to_modify['Nom']} {player_to_modify['Prenom']} \n"
			f"Nouveau classement : {player_to_modify['Classement']}"
			)
		player_db.update({'Classement': int(new_ranking)}, doc_ids=[int(player_id)])
		time.sleep(2.5)
		self.main_menu()

	#Ajout des infos à la bdd
	def add_to_database(self, infos_player):
		player = Player(infos_player[0],
						infos_player[1],
						infos_player[2],
						infos_player[3],
						infos_player[4]
						)
		player_id = player_db.insert(player.serialized())
		player_db.update({'ID du joueur': player_id}, doc_ids=[player_id])
		#player_db.update({'Score': tournament_score}, doc_ids=[player_id])
		time.sleep(2)