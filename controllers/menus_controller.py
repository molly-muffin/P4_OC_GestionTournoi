class CreateMenus:
    """Créer le menu et les sous menus"""

    main_menu = [("1", "Menu Joueur"),
                 ("2", "Menu Tournoi"),
                 ("3", "Quitter")]

    player_menu = [("1", "Créer un joueur"),
                   ("2", "Mettre à jour le classement d'un joueur"),
                   ("3", "Afficher un rapport"),
                   ("4", "Retour au menu principal")]

    tournament_menu = [("1", "Créer un nouveau tournoi"),
                       ("2", "Lancer un tournoi existant"),
                       ("3", "Reprendre un tournoi en cours"),
                       ("4", "Afficher un rapport"),
                       ("5", "Retour au menu principal")]

    time_controller_menu = [("1", "Bullet"),
                            ("2", "Blitz"),
                            ('3', "Coup rapide")]

    players_report_menu = [("1", "Par ordre alphabétique"),
                           ("2", "Par ordre de classement"),
                           ("3", "Pour revenir au menu principal")]

    tournaments_report_menu = [("1", "Afficher tous les tournois"),
                               ("2", "Choisir un tournoi"),
                               ("3", "Retour au menu principal")]

    tournaments_report_menu_2 = [("1", "Afficher les joueurs"),
                                 ("2", "Afficher les tours"),
                                 ("3", "Afficher les matchs"),
                                 ("4", "Retour au menu principal")]

    def __call__(self, display_menu):
        """Afficher un menu et demander à l'utilisateur de choisir"""
        for line in display_menu:
            print(line[0] + " : " + line[1])
        while True:
            entry = input(" --> ")
            for line in display_menu:
                if entry == line[0]:
                    return str(line[0])
            print("Vous devez entrer le chiffre correspondant")
