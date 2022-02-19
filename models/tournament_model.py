#############
#  LIBRARY  #
#############
from tinydb import TinyDB


############
#  SCRIPT  #
############
from views import main_view
from models import player_model


###############
#  VARIABLES  #
###############
tournament_db = TinyDB("models/tournaments.json")


######################
#  CLASS & FUNCTION  #
######################
class Tournament(object):
    """Instancier un tournoi"""
    # méthode init
    def __init__(self,
                 tournament_name=None,
                 place=None,
                 date=None,
                 rounds=4,
                 time_controller=None,
                 description=None,
                 list_id_players=None,
                 list_of_rounds=[],
                 tournament_id=None):
        # attributs
        self.tournament_name = tournament_name
        self.place = place
        self.date = date
        self.rounds = rounds
        self.time_controller = time_controller
        self.description = description
        self.list_id_players = list_id_players
        self.list_of_rounds = list_of_rounds
        self.tournament_id = tournament_id

    # sérialisation
    def serialized(self):
        tournament_details = {}
        tournament_details['Nom du tournoi'] = self.tournament_name
        tournament_details['Lieu'] = self.place
        tournament_details['Date'] = self.date
        tournament_details['Nombre de tours'] = self.rounds
        tournament_details['Gestion du temps'] = self.time_controller
        tournament_details['Description'] = self.description
        tournament_details['ID des joueurs'] = self.list_id_players
        tournament_details['ID des tours'] = self.list_of_rounds
        tournament_details['ID du tournoi'] = self.tournament_id
        return tournament_details

    # désérialisation
    def unserialized(self, serialized_tournament):
        tournament_name = serialized_tournament['Nom du tournoi']
        place = serialized_tournament['Lieu']
        date = serialized_tournament['Date']
        rounds = serialized_tournament['Nombre de tours']
        time_controller = serialized_tournament['Gestion du temps']
        description = serialized_tournament['Description']
        list_id_players = serialized_tournament['ID des joueurs']
        list_of_rounds = serialized_tournament['ID des tours']
        tournament_id = serialized_tournament['ID du tournoi']
        return Tournament(tournament_name,
                          place,
                          date,
                          rounds,
                          time_controller,
                          description,
                          list_id_players,
                          list_of_rounds,
                          tournament_id)

    # méthode repr --> retourne le nom, le lieu et la liste des tours
    def __repr__(self):
        return f"{self.tournament_name} - {self.place}\n - {self.list_of_rounds}\n"

    # Ajout des infos à la bdd
    def add_to_database(self, infos_tournament):
        tournament = Tournament(infos_tournament[0],
                                infos_tournament[1],
                                infos_tournament[2],
                                infos_tournament[3],
                                infos_tournament[4],
                                infos_tournament[5],
                                infos_tournament[6])
        tournament_id = tournament_db.insert(tournament.serialized())
        tournament_db.update({'ID du tournoi': tournament_id}, doc_ids=[tournament_id])


class Round(object):
    """Instancier un Round"""
    # méthode init
    def __init__(self,
                 name=None,
                 start=None,
                 end=None,
                 list_of_finished_matchs=None):
        # attributs
        self.name = name
        self.start = start
        self.end = end
        self.list_of_finished_matchs = list_of_finished_matchs
        self.list_of_rounds = []

    # sérialisation
    def serialized(self):
        round_details = {}
        round_details['Nom'] = self.name
        round_details['Debut'] = self.start
        round_details['Fin'] = self.end
        round_details['Matchs'] = self.list_of_finished_matchs
        return round_details

    # désérialisation
    def unserialized(self, serialized_round):
        name = serialized_round['Nom']
        start = serialized_round['Debut']
        end = serialized_round['Fin']
        list_of_finished_matchs = serialized_round['Matchs']
        return Round(name,
                     start,
                     end,
                     list_of_finished_matchs)

    # méthode repr --> retourne le nom, le time code de début et de fin du tour
    def __repr__(self):
        return f"{self.name} - Début : {self.start}. Fin : {self.end}."

    # Lancer un tour et ajouter les scores pour chaque joueur de chaque matchs
    def run(self, sorted_players_list, tournament_object):
        self.view = main_view.RoundDisplay()
        self.list_of_rounds = []
        self.list_of_finished_matchs = []
        self.players_db = player_model.player_db
        # Round + 1
        self.name = "Round " + str(len(tournament_object.list_of_rounds) + 1)
        # Instanciation de "match" dans la liste "list_of_rounds"
        for i in range(0, int(len(sorted_players_list) / 2)):
            match_instance = Match(name=self.name, player_1=sorted_players_list[0], player_2=sorted_players_list[1])
            Match.MATCH_NUMBER += 1
            self.list_of_rounds.append(match_instance)
            del sorted_players_list[0:2]
        # Liste des tours
        self.view.display_tour(self.name, self.list_of_rounds)
        self.start, self.end = self.view.display_tournament_time()
        for match in self.list_of_rounds:

            valid_score_1 = False
            # Demande de score du joueur 1
            while not valid_score_1:
                score_1 = input(f"Entrez le score de {match.player_1} : \n --> ")
                if score_1.isdigit() and 0 <= int(score_1) <= 1:
                    valid_score_1 = True
                    float(score_1)
                    match.score_1 = float(score_1)
                    new_score_1 = match.player_1.tournament_score + match.score_1
                    update_score_1 = self.players_db.get(doc_id=int(match.player_1.player_id))
                    update_score_1['Score'] = new_score_1
                    self.players_db.update({'Score': int(new_score_1)}, doc_ids=[int(match.player_1.player_id)])
                    print(match.player_1.tournament_score)
                else:
                    print("Vous devez écrire 0, 0.5, ou 1.")

            valid_score_2 = False
            # Demande de score du joueur 1
            while not valid_score_2:
                score_2 = input(f"Entrez le score de {match.player_2} : \n --> ")
                if score_2.isdigit() and 0 <= int(score_2) <= 1:
                    valid_score_2 = True
                    float(score_2)
                    match.score_2 = float(score_2)
                    new_score_2 = match.player_2.tournament_score + match.score_2
                    update_score_2 = self.players_db.get(doc_id=int(match.player_2.player_id))
                    update_score_2['Score'] = new_score_2
                    self.players_db.update({'Score': int(new_score_2)}, doc_ids=[int(match.player_2.player_id)])
                    print(match.player_2.tournament_score)
                else:
                    print("Vous devez écrire 0, 0.5, ou 1.")
            # Instencier la liste des matchs terminés
            self.list_of_finished_matchs.append(([match.player_1.player_id, match.score_1],
                                                [match.player_2.player_id, match.score_2]))
        return Round(self.name, self.start, self.end, self.list_of_finished_matchs)


class Match(object):
    """Instancier un Match"""
    MATCH_NUMBER = 1

    # méthode init
    def __init__(self,
                 name=None,
                 player_1=None,
                 score_1=0,
                 player_2=None,
                 score_2=0):
        # attributs
        self.name = "Match" + str(Match.MATCH_NUMBER)
        self.player_1 = player_1
        self.score_1 = score_1
        self.player_2 = player_2
        self.score_2 = score_2

    # méthode str --> retourne le nom du match et les deux joueurs
    def __str__(self):
        return f"{self.name} : {self.player_1} ** CONTRE ** {self.player_2}."
