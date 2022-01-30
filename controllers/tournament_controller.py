#############
#  LIBRARY  #
#############
from operator import itemgetter
from operator import attrgetter
import pandas as pd
import copy
import time

############
#  SCRIPT  #
############
from views import main_view
from controllers import main_controller
from controllers import menus_controller
from models import tournament_model
from models import player_model

######################
#  CLASS & FUNCTION  #
######################
class NewTournament(object):
	"""Ajout des informations pour créer un tournoi + Ajout du tournoi à la bdd """
	def __init__(self):
		self.create_menu = menus_controller.CreateMenus()
		self.infos_tournament = []
		self.players_in_tournament = []
		self.list_id_players = []
		self.players_serialized = []
		self.player = player_model.Player()
		self.main_menu = main_controller.MainMenu()
		self.tournament = tournament_model.Tournament()

	def __call__(self):
		self.infos_tournament.append(self.add_tournament_name())
		self.infos_tournament.append(self.add_place())
		self.infos_tournament.append(self.add_date())
		self.infos_tournament.append(self.add_rounds())
		self.infos_tournament.append(self.add_time_controller())
		self.infos_tournament.append(self.add_description())
		self.add_players_to_tournament()
		self.infos_tournament.append(self.players_in_tournament)
		self.tournament.add_to_database(self.infos_tournament)
		self.main_menu()

	def add_tournament_name(self):
		valid_tournament_name = False
		#Demande le nom du tournoi (pas vide)
		while not valid_tournament_name:
			tournament_name = input("Ecrire le nom du tournoi : \n --> ")
			if tournament_name != "":
				valid_tournament_name = True
			else:
				print("Vous devez écrire un nom.")
		return tournament_name

	def add_place(self):
		valid_place = False
		#Demande le lieu du tournoi (pas vide)
		while not valid_place:
			place = input("Ecrire l'endroit où se déroule le tournoi : \n --> ")
			if place != "":
				valid_place = True
			else:
				print("Vous devez écrire un lieu.")
		return place

	def add_date(self):
		date_list = []
		valid_day = False
		#Demande le jour du tournoi (nombre à 2 chiffres <=31)
		while not valid_day:
			self.day = input("Ecrire le jour du tournoi : \n --> ")
			if self.day.isdigit() and int(self.day) < 32 and len(self.day) == 2:
				valid_day = True
				date_list.append(self.day)
			else:
				print("Vous devez écrire un nombre à 2 chiffres <= 31.")

		valid_month = False
		#Demande le mois du tournoi (nombre à 2 chiffres <=12)
		while not valid_month:
			self.month = input("Ecrire le mois du tournoi (En chiffre) : \n --> ")
			if self.month.isdigit() and int(self.month) < 13 and len(self.month) == 2:
				valid_month = True
				date_list.append(self.month)
			else:
				print("Vous devez écrire un nombre à 2 chiffres <= 12.")

		valid_year = False
		#Demande l'année du tournoi (nombre à 4 chiffres <=2022)
		while not valid_year:
			self.year = input("Ecrire l'année du tournoi : \n --> ")
			if self.year.isdigit() and int(self.year) < 2023 and len(self.year) == 4:
				valid_year = True
				date_list.append(self.year)
			else:
				print("Vous devez écrire un nombre à 4 chiffres <= 2022.")
		return f"{date_list[0]}/{date_list[1]}/{date_list[2]}"

	def add_rounds(self):
		#Nombre de tour par défault = 4
		rounds = 4
		print("Le nombre de tours par défaut est de 4 \nSouhaitez-vous changer ce nombre ? \n")
		valid_number = False
		#Demande du nombre de tour voulu
		while not valid_number:
			choice = input("Ecrire 'O' pour modifier, ou 'N' pour garder le nombre tours par défault : \n --> ")
			if choice == "O":
				rounds = input("Ecrire le nombre de rounds : \n --> ")
				if rounds.isdigit() and int(rounds) >= 0:
					valid_number = True
				else:
					print("Vous devez écrire un nombre entier positif.")
			if choice == "N":
				valid_number = True
		return rounds

	def add_time_controller(self):
		print("Choisissez le contrôle du temps:")
		time_controller = None
		entry = self.create_menu(self.create_menu.time_controller_menu)
		#Demande de la gestion du temps voulue
		if entry == "1":
			#1 = 2 min par tour	
			time_controller = "Bullet"
		if entry == "2":
			#2 = 3 min par tour	
			time_controller = "Blitz"
		if entry == "3":
			#3 = 5 min par tour	
			time_controller = "Coup rapide"
		return time_controller

	def add_description(self):
		description = input("Ecrire une description du tournoi : \n --> ")
		return description

	def add_players_to_tournament(self):
		"""Ajouter les identifiants des joueurs sélectionnés dans une liste, puis retourner la liste"""
		main_view.ClearScreen()
		id_choice = None
		print(
			"\n************ Ajouter des joueurs au tournoi ***********\n"
			"***** Vous devez entrer un nombre de joueurs pair *****\n")
		players_dispo = player_model.player_db
		for player in players_dispo:
			print(f"{player.doc_id} - {player['Nom']} {player['Prenom']} - Classement : {player['Classement']}")

		#Demande id du joueur à ajouter
		valid_id = False
		while not valid_id:
			id_choice = input("\nEcrire le numéro du joueur que vous souhaitez ajouter :\n --> ")
			try:
				int(id_choice)
			except Exception:
				print("Vous devez écrire un nombre entier positif.")
			else:
				valid_id = True
		id_choice = int(id_choice)

		if id_choice <= 0 or id_choice > len(player_model.player_db):
			print("\nVous devez choisir un joueur dans la liste des joueurs disponibles.")
			print("\nJoueurs dans le tournoi : " + str(self.list_id_players))
			time.sleep(2)
			self.add_players_to_tournament()

		if id_choice in self.list_id_players:
			print("\nVous avez déjà sélectionné ce joueur dans ce tournoi.")
			print("\nJoueurs dans le tournoi : " + str(self.list_id_players))
			time.sleep(2)
			self.add_players_to_tournament()

		#Ajouter puis afficher les joueurs
		self.list_id_players.append(id_choice)
		print("Joueurs dans le tournoi : " + str(self.list_id_players))
		time.sleep(1)

		valid_add_player_choice = False
		while not valid_add_player_choice:
			add_player_choice = input("\nVoulez-vous ajouter un joueur ? \nAppuyer sur 'O' pour ajouter un joueur, ou 'N' pour poursuivre : \n --> ")
			if add_player_choice == "O":
				valid_add_player_choice = True
			elif add_player_choice == "N":
				return
			else:
				print("Appuyez sur 'O' pour ajouter un joueur ou 'N' pour sortir.")
		self.add_players_to_tournament()

		# Instancier une liste de joueurs triée par classsement.
		for id in self.list_id_players:
			player = player_model.player_db.get(doc_id=id)
			self.players_serialized.append(player)
		self.players_serialized.sort(key=itemgetter("Classement"), reverse=True)
		self.list_id_players.clear()

		for player in self.players_serialized:
			self.list_id_players.append(player.doc_id)
		self.infos_tournament.append(self.list_id_players.copy())




class StartTournament(object):
	"""Démarer un tournoi"""
	MATCHS_PLAYED = []
	TOURS_PLAYED = []

	def __call__(self):
		self.sorted_players = []
		self.tournament_menu_controller = main_controller.TournamentMenuController()
		self.round = tournament_model.Round()
		self.view_final_scores = main_view.EndTournamentDisplay()
		self.main_menu = main_controller.MainMenu()
		self.tournament_object = self.select_a_tournament()
		self.sorted_players = self.sort_player_first_tour(self.tournament_object)
		self.tournament_object.list_of_rounds.append(self.round.run(self.sorted_players, self.tournament_object))
		self.save_tournament_statement(self.tournament_object)

		for tour in range(int(self.tournament_object.rounds) - 1):
			self.sorted_players.clear()
			self.sorted_players = self.sort_players_by_score(self.tournament_object.list_of_rounds[tour])
			self.tournament_object.list_of_rounds.append(self.round.run(self.sorted_players, self.tournament_object))
			self.save_tournament_statement(self.tournament_object)

		self.view_final_scores(self.tournament_object)
		self.main_menu()

	def save_tournament_statement(self, tournament_object):
		'''Sauvegarde du tournoi en cours'''
		self.main_menu = main_controller.MainMenu()
		db_tournament = tournament_model.tournament_db
		tours_table = db_tournament.table("rounds")
		tour_object = tournament_object.list_of_rounds[-1]
		tour_serialized = tour_object.serialized()
		tour_serialized['Matchs'] = tour_object.list_of_finished_matchs
		tour_id = tours_table.insert(tour_serialized)
		StartTournament.TOURS_PLAYED.append(tour_id)
		db_tournament.update({"ID des tours": StartTournament.TOURS_PLAYED}, doc_ids=[tournament_object.tournament_id])
		valid_choice = False
		#Demande de sauvegarde du tournoi en cours avant de quitter ou continuer 
		while not valid_choice:
			choice = input("Voulez vous sauvegarder et quitter le tournoi en cours ?  \n 'O' pour valider, 'N' pour continuer : \n --> ")
			if choice == 'O':
				valid_choice = True
				self.main_menu()
			elif choice == 'N':
				valid_choice = True
				break
			else:
				print("Vous devez écrire 'O' pour valider ou 'N' pour continuer.")
				continue

	def load_tournament_statement(self):
		'''Choisir un tournoi et calculer le nombre de tours restant'''
		sorted_players = []
		self.tournament = tournament_model.Tournament()
		self_display_tournament = main_view.LoadTournamentDisplay()
		self.main_menu = main_controller.MainMenu()
		self.round = tournament_model.Round()
		self.view_final_scores = main_view.EndTournamentDisplay()
		db_tournament = tournament_model.tournament_db
		tours_table = db_tournament.table("rounds")
		tours_instances = []
		#Demande quel tournoi continuer
		if self_display_tournament():
			valid_entry = False
			while not valid_entry:
				choice = input("Ecrire le chiffre correspondant au tournoi que vous souhaitez sélectionner : \n --> ")
				try:
					int(choice)
					valid_entry = True
				except Exception:
					print("Vous devez écrire un chiffre correspondant à un tournoi existant.")
				else:
					select_tournament = tournament_model.tournament_db.get(doc_id=int(choice))
					for tour in select_tournament["ID des tours"]:
						tour_serialized = tours_table.get(doc_id=tour)
						tour_object = self.round.unserialized(tour_serialized)
						tours_instances.append(tour_object)
					select_tournament["ID des tours"] = tours_instances
					tournament_object = self.tournament.unserialized(select_tournament)
		else:
			print("Pas de tournoi en cours, retour au menu principal.")
			time.sleep(1)
			self.main_menu()

		for tour in range(int(tournament_object.rounds) - len(tournament_object.list_of_rounds)):
			sorted_players.clear()
			sorted_players = self.sort_players_by_score(tournament_object.list_of_rounds[tour])
			tournament_object.list_of_rounds.append(self.round.run(sorted_players, tournament_object))
			self.save_tournament_statement(tournament_object)
		self.view_final_scores(tournament_object)
		self.main_menu()


	def select_a_tournament(self):
		"""Choisir un tournoi"""
		self.tournament = tournament_model.Tournament()
		self.display_tournaments = main_view.TournamentDisplay()
		self.main_menu = main_controller.MainMenu()
		if self.display_tournaments():
			valid_entry = False
			#Demande quel tournoi choisir
			while not valid_entry:
				choice = input("Ecrire le chiffre correspondant au tournoi que vous souhaitez sélectionner : \n --> ")
				try:
					choice.isdigit() is False
					int(choice) < len(tournament_model.tournament_db)
					int(choice) <= 0
				except Exception:
					print("Vous devez écrire un chiffre correspondant à un tournoi.")
				else:
					select_tournament = tournament_model.tournament_db.get(doc_id=int(choice))
					tournament_object = self.tournament.unserialized(select_tournament)
					return tournament_object
		else:
			print("Pas de tournoi créé, veuillez créer un tournoi.")
			time.sleep(1)
			self.main_menu()

	def sort_player_first_tour(self, tournament):
		"""Joueur par trier par classement"""
		self.player = player_model.Player()
		sorted_players = []
		players_instances = []

		for id in tournament.list_id_players:
			player = player_model.player_db.get(doc_id=id)
			player = self.player.unserialized(player)
			players_instances.append(player)

		for player in players_instances:
			player_1 = player
			index_player_1 = players_instances.index(player)
			if index_player_1 + len(tournament.list_id_players) / 2 < len(tournament.list_id_players):
				index_player_2 = index_player_1 + int(len(tournament.list_id_players) / 2)
				player_2 = players_instances[index_player_2]
				sorted_players.append(player_1)
				sorted_players.append(player_2)
				self.MATCHS_PLAYED.append({player_1.player_id, player_2.player_id})
			else:
				pass
		return sorted_players

	def sort_players_by_score(self, tour_instance):
		"""Joueur par trier par score"""
		self.player = player_model.Player()
		players = []
		players_sorted_by_score = []
		players_sorted_flat = []
		players_instance = []
		match_to_try = set()

		for match in tour_instance.list_of_finished_matchs:
			for player in match:
				players.append(player)
		players_sorted_by_score = copy.copy(players)

		for player in players_sorted_by_score:
			players_sorted_flat.append(player[0])
		players_sorted_by_score.clear()

		for player_id in players_sorted_flat:
			player = player_model.player_db.get(doc_id=player_id)
			players_instance.append(self.player.unserialized(player))
		players_instance.sort(key=attrgetter('tournament_score', 'ranking'), reverse=True)

		for player_1 in players_instance:
			if player_1 in players_sorted_by_score:
				continue
			else:
				try:
					player_2 = players_instance[players_instance.index(player_1) + 1]
				except Exception:
					break
			match_to_try.add(player_1.player_id)
			match_to_try.add(player_2.player_id)

			while match_to_try in self.MATCHS_PLAYED:
				# compare match_to_try with matchs already played
				print(f"Le match {player_1} ** CONTRE ** {player_2} a déjà eu lieu")
				time.sleep(1)
				match_to_try.remove(player_2.player_id)
				try:
					player_2 = players_instance[players_instance.index(player_2) + 1]
				except Exception:
					break
				match_to_try.add(player_2)
				continue

			else:
				print(f"Ajout du match {player_1} ** CONTRE ** {player_2}")
				players_sorted_by_score.append(player_1)
				players_sorted_by_score.append(player_2)
				players_instance.pop(players_instance.index(player_2))
				self.MATCHS_PLAYED.append({player_1.player_id, player_2.player_id})
				match_to_try.clear()
				time.sleep(1)

		return players_sorted_by_score


class TournamentReport(object):
	"""Afficher les rapports de tournoi"""
	def __call__(self):
		self.clear = main_view.ClearScreen()
		self.create_menu = menus_controller.CreateMenus()
		self.display_tournament = main_view.DisplayTournamentsReport()
		self.display_player = main_view.DisplayPlayersReport()
		self.main_menu = main_controller.MainMenu()
		self.players_database = player_model.player_db
		self.player = player_model.Player()
		player_serialized = []
		self.tournament_db = tournament_model.tournament_db
		self.tournament = tournament_model.Tournament()
		tour_table = self.tournament_db.table("rounds")
		tournament_serialized = []
		tournament_objects = []

		for tournament in self.tournament_db:
			tournament_objects.append(tournament)
			tournament_serialized.append(self.tournament.unserialized(tournament))
		self.clear()
		self.display_tournament()
		entry = self.create_menu(self.create_menu.tournaments_report_menu)

		# Afficher tous les tournois
		if entry == "1":
			for tournament in tournament_serialized:
				for id in tournament.list_id_players:
					player = self.players_database.get(doc_id=id)
					player_serialized.append(self.player.unserialized(player))
			self.display_tournament.display_tournaments(tournament_serialized, player_serialized)
			player_serialized.clear()
			self.main_menu()
		# Choisir un tournoi
		if entry == "2":
			self.display_tournament.choose_a_tournament(tournament_serialized)
			valid_choice = True
			while valid_choice:
				choice_id = input("Ecrire le chiffre correspondant au tournoi que vous souhaitez sélectionner : \n --> ")
				for tournament in tournament_objects:
					if int(choice_id) == tournament.doc_id:
						tournament_object = self.tournament_db.get(doc_id=int(choice_id))
						tournament_object = self.tournament.unserialized(tournament_object)
						if tournament_object.list_of_rounds == []:
							print("\nLe tournoi n'a pas encore eu lieu, vous ne pouvez pas afficher les résultats.\n")
							time.sleep(1)
						else:
							entry = self.create_menu(self.create_menu.tournaments_report_menu_2)
							# Afficher les joueurs
							if entry == "1":
								entry = self.create_menu(self.create_menu.players_report_menu)

								# Afficher les joueurs par ordre alphabetique
								if entry == "1":
									for id in tournament_object.list_id_players:
										player = self.players_database.get(doc_id=int(id))
										player_serialized.append(self.player.unserialized(player))
									player_serialized.sort(key=attrgetter("name"))
									self.display_player.display_alphabetical(player_serialized)
									player_serialized.clear()
									TournamentReport.__call__(self)

								# Afficher les joueurs par classement
								if entry == "2":
									for id in tournament_object.list_id_players:
										player = self.players_database.get(doc_id=int(id))
										player_serialized.append(self.player.unserialized(player))
									player_serialized.sort(key=attrgetter("ranking"))
									self.display_player.display_ranking(player_serialized)
									player_serialized.clear()
									input("Appuyez sur une touche pour revenir au menu rapport de tournoi.")
									TournamentReport.__call__(self)

							# Afficher les tours
							if entry == "2":
								for tour in tournament_object.list_of_rounds:
									tr = tour_table.get(doc_id=tour)
									print(f"{tr['Nom']} - Début: {tr['Debut']} - Fin : {tr['Fin']}\n")
								input("Appuyez sur une touche pour revenir au menu rapport de tournoi.")
								TournamentReport.__call__(self)

							# Afficher les matchs
							if entry == "3":
								for tour in tournament_object.list_of_rounds:
									tr = tour_table.get(doc_id=tour)
									print(f"**************** {tr['Nom']} ****************")
									for match in tr['Matchs']:
										player_1 = match[0][0]
										player_1 = self.players_database.get(doc_id=player_1)
										score_player_1 = match[0][1]
										player_2 = match[1][0]
										player_2 = self.players_database.get(doc_id=player_2)
										score_player_2 = match[1][1]
										print(
											f"{player_1['Nom']} {player_1['Prenom']} ** CONTRE ** {player_2['Nom']} {player_2['Prenom']}\n"
											f"Score : {score_player_1} ** {score_player_2}\n")

								input("Appuyez sur une touche pour revenir au menu rapport de tournoi.")
								TournamentReport.__call__(self)

							# Retour au menu principal
							if entry == "4":
								valid_choice = False
								self.main_menu()

		# Retour au menu principal
		if entry == "3":
			valid_choice = False
			self.main_menu()
		print("Vous devez écrire un chiffre correspondant à un tournoi.")