from logique import *
if MODE_GRAPHIQUE:
    from interface import *
import random
import time


# Variables globales
finPartie = True
listePositions = []
couleurJoueur = ''
victoires = [0] * 3  # Jaunes, Rouges, Nulles
blocageJoueur = False



def clic(event):
    "Gestion du clic de souris"
    global finPartie
    global listePositions
    global couleurJoueur
    global victoires
    #global blocageJoueur  # Indispensable pour les cas où l'on clique trop vite
    #if not blocageJoueur:
    if finPartie:
            #blocageJoueur = True
        listePositions = initialise_liste_jetons()
        destruction_jetons()
        efface_message_fenetre()
        fenetreJeu.update()
        time.sleep(1)
        couleurJoueur = rd.choice(['yellow', 'red'])
        # Affiche joueur qui commence
        affiche_joueur_qui_commence_terminal(couleurJoueur)
        affiche_joueur_qui_commence_fenetre(couleurJoueur)
        finPartie = False
            #blocageJoueur = False
    else:
        x = event.x
        colonne = col = 0
        while col < NB_COLONNES:
            col = col + 1
            ray = rayon()
            if x > col*ESPACEMENT+2*(col-1)*ray and x < col*ESPACEMENT+2*col*ray:
                colonne = col
        if (colonne and not colonne_pleine(listePositions, colonne)):
                #blocageJoueur = True
            listePositions = jouer(listePositions, couleurJoueur, colonne)
            finPartie, couleurJoueur, victoires = fin_partie(listePositions, couleurJoueur, victoires)  # Teste si la partie est finie
            if finPartie:
                    # Bilan
                analyse_victoire(victoires)  # Jaunes, Rouges, Nulles
                affiche_victoires_fenetre(victoires)  # Jaunes, Rouges, Nulles
                #blocageJoueur = False



# La méthode bind() permet de lier un évènement avec une fonction
grille.bind('<Button-1>', clic)


finPartie = False
listePositions = initialise_liste_jetons()
couleurJoueur = rd.choice(['yellow', 'red'])
affiche_joueur_qui_commence_terminal(couleurJoueur)
affiche_joueur_qui_commence_fenetre(couleurJoueur)
