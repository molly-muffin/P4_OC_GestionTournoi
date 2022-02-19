#############
#  LIBRARY  #
#############
from operator import attrgetter


############
#  SCRIPT  #
############
from controllers import main_controller
from controllers import menus_controller
from models import player_model
from views import main_view


######################
#  CLASS & FUNCTION  #
######################
class NewPlayer:
    """Ajout des informations pour créer un joueur + Ajout du joueur à la bdd """
    def __init__(self):
        super(NewPlayer, self).__init__()
        self.infos_player = []
        self.infos_title = ["Nom", "Prénom", "Anniversaire", "Genre", "Classement"]
        self.main_menu = main_controller.MainMenu()

    def __call__(self):
        self.player_model = player_model.Player()
        self.infos_player.append(self.add_name())
        self.infos_player.append(self.add_first_name())
        self.infos_player.append(self.add_birthay_details())
        self.infos_player.append(self.add_sexe())
        self.infos_player.append(self.add_ranking())
        if self.valid_player():
            self.player_model.add_to_database(self.infos_player)
        self.infos_player.clear()
        self.main_menu()

    def add_name(self):
        valid_name = False
        # Demande le nom du joueur (ni vide ni nombres)
        while not valid_name:
            name = input("Ecrire le nom de famille du joueur : \n --> ")
            if name != "" and not name.isdigit():
                valid_name = True
            else:
                print("Vous devez écrire un nom de famille (aucun chiffre autorisé).")
        return name

    def add_first_name(self):
        valid_first_name = False
        # Demande le prénom du joueur (ni vide ni nombres)
        while not valid_first_name:
            first_name = input("Ecrire le prénom du joueur : \n --> ")
            if first_name != "" and not first_name.isdigit():
                valid_first_name = True
            else:
                print("Vous devez écrire un prénom (aucun chiffre autorisé).")
        return first_name

    def add_birthay_details(self):
        birthday_list = []
        valid_day = False
        # Demande le jour de naissance du joueur (nombre à 2 chiffres <=31)
        while not valid_day:
            self.birth_day = input("Ecrire le jour de naissance du joueur : \n --> ")
            if self.birth_day.isdigit() and int(self.birth_day) < 32 and len(self.birth_day) == 2:
                valid_day = True
                birthday_list.append(self.birth_day)
            else:
                print("Vous devez écrire un nombre à 2 chiffres inférieur ou égal à 31.")

        valid_month = False
        # Demande le mois de naissance du joueur (nombre à 2 chiffres <=12)
        while not valid_month:
            self.birth_month = input("Ecrire le mois de naissance du joueur (en chiffre) : \n --> ")
            if self.birth_month.isdigit() and int(self.birth_month) < 13 and len(self.birth_month) == 2:
                valid_month = True
                birthday_list.append(self.birth_month)
            else:
                print("Vous devez écrire un nombre à 2 chiffres inférieur ou égal à 12.")

        valid_year = False
        # Demande l'année de naissance du joueur (nombre à 4 chiffres <=2022)
        while not valid_year:
            self.birth_year = input("Ecrire l'année de naissance du joueur : \n --> ")
            if self.birth_year.isdigit() and int(self.birth_year) < 2023 and len(self.birth_year) == 4:
                valid_year = True
                birthday_list.append(self.birth_year)
            else:
                print("Vous devez écrire un nombre à 4 chiffres inférieur ou égal à 2022.")

        return f"{birthday_list[0]}/{birthday_list[1]}/{birthday_list[2]}"

    def add_sexe(self):
        valid_sexe = False
        view_sexe = None
        # Demande le genre du joueur (H=Homme F=Femme)
        while not valid_sexe:
            sexe = input("Choisissez le genre du joueur \n 'H' pour un homme \n 'F' pour une femme : \n --> ")
            if sexe == "H":
                valid_sexe = True
                view_sexe = "Homme"
            elif sexe == "F":
                valid_sexe = True
                view_sexe = "Femme"
            else:
                print("Vous devez écrire un genre ('H' pour Homme ou 'F' pour Femme).")
        return view_sexe

    def add_ranking(self):
        valid_ranking = False
        # Demande le classement du joueur (nombre > 0)
        while not valid_ranking:
            ranking = input("Ecrire le classement du joueur : \n --> ")
            if ranking.isdigit() and int(ranking) >= 0:
                valid_ranking = True
            else:
                print("Vous devez écrire un nombre entier positif.")
        return int(ranking)

    def valid_player(self):
        main_view.FrameDisplay.display_datas_in_a_frame(self.infos_player, self.infos_title)
        valid_choice = False
        # Demande la validation des détails du joueur (nombre > 0)
        while not valid_choice:
            choice = input("Validez-vous ce joueur ? \n 'O' pour valider, 'N' pour recommencer \n --> ")
            if choice == "O":
                valid_choice = True
            elif choice == "N":
                main_controller.MainMenu()
            else:
                print("Vous devez entrer 'O' pour valider ou 'N' pour recommencer.")
        return valid_choice


class PlayerReport:
    """Afficher les rapports des joueurs"""
    def __call__(self):
        self.main_menu = main_controller.MainMenu()
        self.create_menu = menus_controller.CreateMenus()
        self.player_display = main_view.DisplayPlayersReport()
        self.players_db = player_model.player_db
        self.player = player_model.Player()
        player_serialized = []

        for player in self.players_db:
            player_serialized.append(self.player.unserialized(player))

        self.player_display()
        entry = self.create_menu(self.create_menu.players_report_menu)
        # Demande le type de rapport voulu
        if entry == "1":
            # 1 = ordre alphabétique
            player_serialized.sort(key=attrgetter("name"))
            self.player_display.display_alphabetical(player_serialized)
            PlayerReport.__call__(self)
        if entry == "2":
            # 2 = ordre de classement
            player_serialized.sort(key=attrgetter("ranking"))
            self.player_display.display_ranking(player_serialized)
            PlayerReport.__call__(self)
        if entry == "3":
            # 3 = retour au menu principal
            self.main_menu()
