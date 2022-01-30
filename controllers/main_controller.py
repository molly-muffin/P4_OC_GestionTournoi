#############
#  LIBRARY  #
#############
import sys

############
#  SCRIPT  #
############
from views import main_view
from controllers import menus_controller
from controllers import player_controller
from models import player_model
from controllers import tournament_controller

######################
#  CLASS & FUNCTION  #
######################
class MainMenu:
	"""Afficher les titres des menus"""
	def __init__(self):
		self.view = main_view.MainDisplay()
		self.clear = main_view.ClearScreen()
		self.create_menu = menus_controller.CreateMenus()
		self.select_controller = None

	def __call__(self):
		self.clear()
		self.view.display_title()
		entry = self.create_menu(self.create_menu.main_menu)

		if entry == "1":
			#Afficher le Menu Joueur
			self.select_controller = PlayerMenuController()
			self.go_to_player_menu_controller()
		if entry == "2":
			#Afficher le Menu Tournoi
			self.select_controller = TournamentMenuController()
			self.go_to_tournament_menu_controller()
		if entry == "3":
			#Quitter l'appli
			self.select_controller = QuitAppController()
			self.go_to_quit_app_controller()

	def go_to_player_menu_controller(self):
		return self.select_controller()
	def go_to_tournament_menu_controller(self):
		return self.select_controller()
	def go_to_quit_app_controller(self):
		return self.select_controller()


class PlayerMenuController(MainMenu):
	"""Afficher les titres des menus dans le menu joueur"""
	def __init__(self):
		super().__init__()
		self.create_player = player_controller.NewPlayer()
		self.players_report = player_controller.PlayerReport()
		self.main_menu = MainMenu()
		self.player_model = player_model.Player()

	def __call__(self):
		entry = self.create_menu(self.create_menu.player_menu)
		if entry == "1":
			#Créer un joueur
			self.select_controller = self.create_player()
		if entry == "2":
			#Mettre à jour le classement d'un joueur
			self.select_controller = self.player_model.update_ranking()
		if entry == "3":
			#Afficher les rapports des joueurs
			self.select_controller = self.players_report()
		if entry == "4":
			#Revenir au menu principal
			self.select_controller = self.main_menu()


class TournamentMenuController(MainMenu):
	"""Afficher les titres des menus dans le menu tournoi"""
	def __init__(self):
		super().__init__()
		self.tournament_report_controller = tournament_controller.TournamentReport()
		self.create_tournament = tournament_controller.NewTournament()
		self.main_menu = MainMenu()
		self.start_tournament = tournament_controller.StartTournament()

	def __call__(self):
		entry = self.create_menu(self.create_menu.tournament_menu)
		if entry == "1":
			#Créer un tournoi
			self.select_controller = self.create_tournament()
		if entry == "2":
			#Commencer un tournoi existant
			self.select_controller = self.start_tournament()
		if entry == "3":
			#Repprendre un tournoi existant
			self.select_controller = self.start_tournament.load_tournament_statement()
		if entry == "4":
			#Afficher les rapports des tournois
			self.select_controller = self.tournament_report_controller()
		if entry == "5":
			#Retour au menu principal
			self.select_controller = self.main_menu()			

class QuitAppController:
	def __call__(self):
		sys.exit()