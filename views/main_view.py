#############
#  LIBRARY  #
#############
from os import system, name
import pandas as pd
import time

############
#  SCRIPT  #
############
from models import player_model
from models import tournament_model

######################
#  CLASS & FUNCTION  #
######################
class MainDisplay:
	def display_title(self):
		"""Affichage de la page d'acceuil"""
		print(
			"******************************************************\n"
			"************** Gestionnnaire de tournoi **************\n"
			"******************************************************\n"
			"******************************************************\n"
			"******************* Menu principal *******************\n"
			"******************************************************\n"
			"* Entrez le numéro correspondant à votre séléction : *\n"
			"******************************************************\n")


class ClearScreen:
	"""Nettoyer le champ"""
	def __call__(self):
		# windows
		if name == 'nt':
			_ = system('cls')
		# mac & linux
		else:
			_ = system('clear')


class FrameDisplay:
	"""Afficher les données écrite par l'utilisteur"""
	def display_datas_in_a_frame(self, data, index=None, columns=None):
		display = pd.DataFrame(self, data, index, columns)
		print("Voici les données que vous avez entrer : \n")
		print(display)


class PlayersDiplay:
	"""Afficher les joueurs de la base de donnée"""
	def __call__(self):
		players_database = player_model.player_db

		for player in players_database:
			print(f"{player.doc_id} - {player['Nom']} {player['Prenom']} - Classement : {player['Classement']}")


class DisplayPlayersReport:
	"""Afficher les joueurs selon un certain classement"""
	def __call__(self):
		print(
			"******************************************************\n"
			"*************** Affichages des joueurs ***************\n"
			"******************************************************\n"
			"************** Afficher les rapports : ***************\n"
			"******************************************************\n")

	#ordre alphabetique	
	def display_alphabetical(self, players_list):
		for player in players_list:
			print(
				f"{player.name} {player.first_name}"
				f" - Classement : {player.ranking} - Score : {player.tournament_score}")
		input("\n Appuyer sur une touche pour revenir au menu rapport. \n")

	#ordre classement
	def display_ranking(self, players_list):
		for player in players_list:
			print(
				f"Classement : {player.ranking} - Score : {player.tournament_score}"
				f" - {player.name} - {player.first_name}")
		input("\n Appuyer sur une touche pour revenir au menu rapport \n")


class TournamentDisplay:
	"""Afficher les détails du tournoi"""
	def __call__(self):
		tournament_not_started = False
		tournaments_database = tournament_model.tournament_db

		for tournament in tournaments_database:
			if tournament['ID des tours'] == []:
				print(f"{tournament.doc_id} - Nom : {tournament['Nom du tournoi']} - Lieu : {tournament['Lieu']}")
				tournament_not_started = True

		return tournament_not_started


class RoundDisplay:
	"""Docstring"""
	def __init__(self):
		self.match = tournament_model.Match()

	def display_tour(self, round_name, list_of_matchs):
		"""Afficher le tour en cours"""
		print(f"\n********************* {round_name} *********************\n")
		for match in list_of_matchs:
			print(match)

	def display_tournament_time(self):
		input("\nAppuyez sur une touche pour commencer le tour. \n")
		#TODO afficher qui contre qui
		start = time.strftime(format("%d/%m/%Y - %Hh%Mm%Ss"))
		print(f"Début du tour : {start} \n")
		input("\nAppuyez sur une touche lorsque le tour est terminé. \n")
		end = time.strftime(format("%d/%m/%Y - %Hh%Mm%Ss"))
		print(f"Fin du tour : {end} \n")
		return start, end


class EndTournamentDisplay:
	"""Afficher les scores à la fin du tournoi"""
	def __call__(self, tournament_instance):
		print(
			"******************************************************\n"
			"******************* Fin du tournoi *******************\n"
			"******************************************************\n"
			"********************* Résultats **********************\n"
			"******************************************************\n"
			)
		print("Résultat final : \n")
		for tour in tournament_instance.list_of_rounds:
			print("************" + tour + "************ \n\n")
			for match in tour.list_of_finished_matchs:
				player_1 = player_model.player_db.get(doc_id=match[0][0])
				score_player_P1 = match[0][1]
				player_2 = player_model.player_db.get(doc_id=match[1][0])
				score_player_P2 = match[1][1]
				print(
					f"{player_1['Nom']} {player_1['Prenom']} ** CONTRE ** {player_2['Nom']} {player_2['Prenom']}\n"
					f"Score : {score_player_P1} ** {score_player_P2}\n")
		input("Appuyez sur une touche pour revenir au menu principal.")


class DisplayTournamentsReport:
	"""Afficher les détails des tournois"""
	def __call__(self):
		print(
			"******************************************************\n"
			"**************** Rapport des tournois ****************\n"
			"******************************************************\n"
			"************** Afficher les rapports : ***************\n"
			"******************************************************\n")

	def display_tournaments(self, tournaments_list, players_list):
		for tournament in tournaments_list:
			print(
				f"{tournament.tournament_name} - {tournament.place} - {tournament.date}\n"
				f"Nombre de tours : {tournament.rounds}\n"
				f"Contrôle du temps : {tournament.time_controller}\n"
				f"Description : {tournament.description}\n")
			for player in players_list:
					print(f"Joueurs : {player.name} - {player.first_name} - Classement : {player.ranking}")
		input("\nAppuyez sur une touche pour revenir au menu principal.")

	def choose_a_tournament(self,tournaments_list):
		for tournament in tournaments_list:
			print(
				f"{tournament.tournament_id} - {tournament.tournament_name} - {tournament.place} - {tournament.date}\n"
				f"Nombre de tours : {tournament.rounds}\n"
				f"Contrôle du temps : {tournament.time_controller}\n"
				f"Description : {tournament.description}\n")


class AskForContinuingTournament:
	def __call__(self, choice):
		valid_choice = True
		while valid_choice:
			choice = input("Voulez vous sauvegarder et quitter le tournoi en cours ?  \n 'O' pour valider, 'N' pour continuer : \n --> ")
			if choice == 'O':
				break
			if choice == 'N':
				pass


class LoadTournamentDisplay:
	def __call__(self):
		tournaments_in_progress = False
		print(
			"******************************************************\n"
			"**************** Reprendre un tournoi ****************\n"
			"******************************************************\n"
			)
		for tournament in tournament_model.tournament_db:
			if tournament["ID des tours"] != []:
				if len(tournament["ID des tours"]) < int(tournament["Nombre de tours"]):
					print(f"{tournament['ID du tournoi']} - {tournament['Nom du tournoi']} {tournament['Lieu']}")
					tournaments_in_progress = True
		return tournaments_in_progress