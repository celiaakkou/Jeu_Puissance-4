import tkinter as tk
import random as rd
import time
import json 
import math


# CHOIX DE L'AFFICHAGE
NB_PARTIES = 1000000  # A adapter (un nombre pair plus grand que 1)
MODE_GRAPHIQUE = True  # True : Pour afficher la grille dans une fenêtre et dans la console
                       # False : Pour afficher la grille dans la console exclusivement
TEMPS_CHUTE = 0.1  # 0.1 pour visualiser la chute des pions sinon 0
LARGEUR_GRILLE = 480  # On peut l'adapter 
ESPACEMENT = LARGEUR_GRILLE / 64  # Espace entre 2 trous de la grille
                                  # Cela signifie que l'espacement enre deux pions serait de 7,5 unités de largeur de grille
                                  # Cela garantit un espacement regulier et uniforme entre les pions sur la grille de jeu
                                  # Et une disposition equilibrée des pions tout en permettant une visibilité de la chute
                                  # l'espace entre les lignes ou les colonnes  sert à une meilleure apparence visuelle.
                                  

# CONTRAINTES DU JEU(LES LIMITATIONS QUI DEFINISSENT LES ACTIONS POSSIBLES DES JOUEURS ET LES CONDITIONS DE VICTOIRE)
NB_COLONNES = 7  # Nombre de colonnes de la grille de jeu
NB_LIGNES = 6  # Nombre de lignes de la grille de jeu
ALIGNEMENT = 4  # Nombre de pions à aligner pour gagner


# CREATION DE LA FENETRE TKINTER
# Création du widget principal ("parent") : fenetreJeu
fenetreJeu = tk.Tk()
# Personnaliser le widget principal
## Titre de la fenetre
fenetreJeu.title("Puissance 4")
## Le fond de la fenetre
fenetreJeu.config(bg="dark slate gray") 


# AFFICHAGE DE LA GRILLE ET DES JETONS DANS LA FENETRE TKINTER
# fonction qui permet de definir la hauteur de la grille en fonction de rayon r des trous de la grille
## 2 * NB_LIGNES * r : la hauteur totale occupée par les trous de la grille. Comme il y a NB_LIGNES lignes
## dans la grille, chaque ligne a besoin d'un espace équivalent à 2 * r (un espace au-dessus et un en dessous) pour accueillir 
## les trous.
## (NB_LIGNES + 1) * ESPACEMENT : la hauteur totale de l'espace entre les lignes de la grille.
## Il y a NB_LIGNES + 1 espacements entre les lignes (un en haut et un en bas, et un entre chaque paire de lignes), chacun ayant
## une hauteur égale à ESPACEMENT.
def hauteur_grille(r):
    """
    Calcule la hauteur de la grille en fonction du rayon r des trous.

    Args:
        r (float): Le rayon des trous.

    Returns:
        float: La hauteur de la grille.

    """
    return 2*NB_LIGNES*r + (NB_LIGNES + 1)*ESPACEMENT

# fonction qui permet de retourner le rayon des trous de la grille et des pions
## (LARGEUR_GRILLE - (NB_COLONNES + 1) * ESPACEMENT) : la largeur totale des trous de la grille.
## Cette largeur totale est divisée par (2 * NB_COLONNES) pour obtenir le rayon. 
## Le facteur 2 est utilisé car il y a deux fois le rayon d'un trou entre chaque paire de colonnes.
def rayon():
    """
    Calcule le rayon des trous de la grille et des pions.

    Returns:
        float: Le rayon des trous et des pions.

    """
    return (LARGEUR_GRILLE - (NB_COLONNES + 1)*ESPACEMENT) / (2*NB_COLONNES)

#  Cette fonction est utilisée pour créer un trou de la grille à une position spécifiée (x, y) avec un rayon r et une couleur c.
## x-r, y-r, x+r, y+r: Ces quatre valeurs sont les coordonnées du rectangle dans lequel le cercle est inscrit. 
## (x-r, y-r) le coin supérieur gauche du rectangle
## (x+r, y+r) le coin inférieur droit du rectangle
## Prenant l'exemple où x = 7,5+r et y = 7,5+r donc on aurait :
## (x-r, y-r) = (7,5+r-r, 7,5+r-r) = (7,5, 7,5)
## (x+r, y+r) = (7,5+r+r, 7,5+r+r) = (7,5+2r, 7,5+2r)
def creation_cercle(x, y, r, c, tag):
    """
    Crée un cercle représentant un trou ou un jeton.

    Args:
        x (float): La coordonnée x du centre du cercle.
        y (float): La coordonnée y du centre du cercle.
        r (float): Le rayon du cercle.
        c (str): La couleur du cercle.
        tag (str): Le tag à associer au cercle.

    Returns:
        identifiant (str): L'identifiant du cercle créé.

    """
    identifiant = grille.create_oval((x-r, y-r), (x+r, y+r), fill=c, width=0, tags=tag) # Le paramètre `tags` est un label
                                                                                        # qu'on donne à la forme ovale pour la 
                                                                                        # manipluler plus tard dans le code
                                                                                        # Ici : tag = "trou" puis tag  "jeton"
    return identifiant

# La fonction parcourt toutes les lignes et toutes les colonnes de la grille, et pour chaque position, elle appelle 
# creation_cercle() pour créer un trou de la grille à cette position.
## Prenant l'exemple de la premiere itération : ligne=1, colonne=1 donc on aurait :
## x = 7,5 + r + (1-1)*(7,5 + 2*r) = 7,5 + r
## y = 7,5 + r + (1-1)*(7,5 + 2*r) = 7,5 + r
## Prenant l'exemple de la deuxieme itération : ligne=1, colonne=2 donc on aurait :
## x = 7,5 + r + (2-1)*(7,5 + 2*r) = 7,5 + r + (7,5 + 2*r)
## y = 7,5 + r + (1-1)*(7,5 + 2*r) = 7,5 + r
def creation_grille(r):
    """
    Crée une grille avec des trous de rayon r.

    La grille est remplie de trous disposés en lignes et colonnes, avec un espacement fixe entre eux.

    Args:
        r (float): Le rayon des trous.

    """
    ligne = 1 # on l'initialise à 1 car on ne doit pas avoir le 0
    while ligne <= NB_LIGNES:
        # Cette boucle s'exécute tant que le numéro de la ligne est inférieur ou égal au nombre de lignes de la grille.
        colonne = 1 # on  l'initialise à 1 car on ne doit pas avoir le 0
        while colonne <= NB_COLONNES:
            # Cette boucle s'exécute tant que le numéro de la colonne est inférieur ou égal au nombre de colonnes de la grille.
            creation_cercle(ESPACEMENT + r + (colonne-1)*(ESPACEMENT + 2*r),
                            ESPACEMENT + r + (ligne-1)*(ESPACEMENT + 2*r),
                            r, 'white', 'trou')
            colonne += 1
        ligne += 1    

# Cette fonction créee un jeton de la couleur spécifiée à la position donnée (colonne, ligne) dans la grille de jeu, elle 
# détermine les coordonnées(x, y)du centre du jeton, appelle la fonction creation_cercle() pour créer le jeton avec ces coordonnées.
## colonne : le numéro de la colonne où le jeton doit être placé.
## ligne : le numéro de la ligne où le jeton doit être placé(c'a'd apres la fin de sa chute !)
## c : la couleur du jeton.
## r : le rayon du jeton
## La formule (NB_LIGNES-ligne+1) : pour inverser la numérotation des lignes, car dans la chute la numérotation commence de bas
## Si ligne=5 : 6-5+1=2 donc le jeton doit etre placé à la ligne 2 car en réalité le joueur a choisi la ligne 2 
def creation_jeton(colonne, ligne, c, r): 
    """
    Crée un jeton de couleur c et de rayon r à la colonne et à la ligne indiquée.

    Args:
        colonne (int): Le numéro de la colonne où placer le jeton.
        ligne (int): Le numéro de la ligne où placer le jeton.
        c (str): La couleur du jeton.
        r (float): Le rayon du jeton.

    Returns:
        indentifiant (str): L'identifiant du jeton créé.

    """
    identifiant = creation_cercle(colonne*(ESPACEMENT+2*r)-r,
                                  (NB_LIGNES-ligne+1)*(ESPACEMENT+2*r)-r,
                                  r, c, 'jeton')
    return identifiant 

# fonction qui permet de déplacer le jeton par ESPACEMENT+2*r pixels vers le bas
## identifiant : l'identifiant du jeton à déplacer
## 0 indique qu'il ne doit pas être déplacé horizontalement. 
## ESPACEMENT+2*r : le nombre de pixels vers le bas que le jeton doit être déplacé.
def mouvement_jeton(identifiant, r):
    """
    Déplace un jeton d'un montant équivalent à l'espacement plus deux fois le rayon.

    Args:
        identifiant (str): L'identifiant du jeton à déplacer.
        ESPACEMENT+2*r : le nombre de pixels vers le bas que le jeton doit être déplacé, où r (float): Le rayon du jeton.

    """
    grille.move(identifiant, 0, ESPACEMENT+2*r)

# Fonction qui affiche un coup joué dans la grille de jeu, avec le jeton descendant jusqu'à la ligne de support spécifiée.
## colonne : la colonne dans laquelle le coup est joué. Le jeton sera placé dans cette colonne.
## ligneSupport : la ligne jusqu'à laquelle le jeton doit descendre. Le jeton commencera sa descente depuis la ligne 
## la plus haute de la grille et descendra jusqu'à atteindre cette ligne de support.
## couleur : la couleur du jeton à afficher.
## La fonction commence par placer un jeton de la couleur spécifiée dans la colonne spécifiée en utilisant la fonction
## creation_jeton(). Ensuite, elle fait descendre progressivement ce jeton jusqu'à la ligne de support spécifiée en utilisant la
## fonction mouvement_jeton().
def affiche_grille_fenetre(colonne, ligneSupport, couleur):
    """
    Affiche le coup joué avec la chute du pion.

    Cette fonction affiche visuellement un coup joué dans la grille en faisant descendre un pion de la colonne spécifiée
    jusqu'à la ligne de support spécifiée.

    Args:
        colonne (int): Le numéro de la colonne où le coup est joué.
        ligneSupport (int): La ligne de support où le pion doit s'arrêter.
        couleur (str): La couleur du pion à afficher.

    """
    ligne = NB_LIGNES
    r = rayon()
    identifiant = creation_jeton(colonne, ligne, couleur, r)
    while ligne > ligneSupport: # Cette boucle s'exécute tant que la ligne actuelle du jeton est supérieure à la ligne de support spécifiée.
        if ligne < NB_LIGNES:
            mouvement_jeton(identifiant, r) # À chaque itération de la boucle, le jeton est déplacé d'une ligne vers le haut 
                                            # par la fonction mouvement_jeton(), simulant ainsi sa descente dans la grille.
        fenetreJeu.update() # Cette instruction met à jour la fenêtre Tkinter pour afficher le mouvement du jeton.
        time.sleep(TEMPS_CHUTE) # Cette instruction fait une pause pendant un court laps de temps, ce qui crée un effet de chute 
                                # plus fluide pour le jeton.
        ligne = ligne - 1 # À chaque itération de la boucle, la variable ligne est décrémentée pour faire progresser le jeton 
                          # vers le haut de la grille( dans puissance 4 le haut de la grille c'est le bas dans tkinter).

# Cette fonction est utilisée pour supprimer tous les jetons de la grille de jeu (fonction appelée à la fin d'une partie).
def destruction_jetons():
    """
    Supprime tous les jetons de la grille.

    """
    grille.delete('jeton')

# Création des widgets "enfants" : bienvenue (Label)
label = tk.Label(fenetreJeu,bg="black",text="BIENVENUE AU JEU PUISSANCE 4",padx=20,pady=20,fg="white",font=("helvetica","20"),
                 borderwidth=10,relief="groove")
# Positionner le widget enfant label par la méthode .grid()
label.grid(row=0,column=1,padx=20,pady=20)

# Création des widgets "enfants" : grille (Canvas)
grille = tk.Canvas(fenetreJeu, width=LARGEUR_GRILLE, height=hauteur_grille(rayon()), background='blue')
creation_grille(rayon())
grille.grid(row=1,column=1)

# Création des widgets "enfants" : message (Label)
message = tk.Label(fenetreJeu,bg="black",text="                  ",fg="pink4",font=("helvetica","20"))
message.grid(row=2,column=1,padx=20,pady=20)

# Création des widgets "enfants" : scoreJaunes (Label)
scoreJaunes = tk.Label(fenetreJeu, text='Jaunes : 0',bg="yellow",font=("helvetica","20"))
scoreJaunes.grid(row=3,column=0)

# Création des widgets "enfants" : scoreRouges (Label)
scoreRouges = tk.Label(fenetreJeu, text='Rouges : 0',bg="red",font=("helvetica","20"))
scoreRouges.grid(row=3,column=2,padx=20, pady=20)

# Creation de bouton Jouer qui permet de choisir le joueur qui commence
boutton_jouer = tk.Button(fenetreJeu,text="  Rejouer  ",font=("helvetica","20"),bg="green",fg="blue")
boutton_jouer.grid(row=4,column=0,padx=20,pady=20)

# Creation de bouton retour en arriere pour annuler un coup joué
#boutton_retour_en_arriere = tk.Button(fenetreJeu,text="Annuler un coup",font=("helvetica","20"),bg="gray",fg="blue")
#boutton_retour_en_arriere.grid(row=4,column=1,padx=20,pady=20)

# creation de bouton sauvegarder pour sauvegarder et charger une partie en cours
boutton_sauvegarder_une_partie = tk.Button(fenetreJeu,text="Sauvegarder une partie",font=("helvetica","20"),bg="gray",fg="blue")
boutton_sauvegarder_une_partie.grid(row=5,column=1,padx=20,pady=20)

# Creation de bouton charger pour charger une partie en cours
#boutton_charger_une_partie = tk.Button(fenetreJeu,text="    Charger une partie    ",font=("helvetica","20"),bg="gray",fg="blue")
#boutton_charger_une_partie.grid(row=6,column=1,padx=20,pady=20)

# Création de bouton quitter, si on souhaite fermer la fenetre de jeu on peut cliquer dessus
boutton_quitter = tk.Button(fenetreJeu,text=" Quitter ",font=("helvetica","20"),bg="brown4",fg="blue",command=fenetreJeu.destroy)
boutton_quitter.grid(row=4,column=2,padx=20,pady=20)


# AFFICHAGE DES MESSAGES DANS LA FENETRE
# fonction qui permet d'afficher le joueur qui commence une partie sur la fenetre tkinter,en modifiant le texte de label message
# cela est choisi au hasard !
def affiche_joueur_qui_commence_fenetre(couleur):
    """
    Affiche le joueur qui commence dans la fenêtre Tkinter.

    Args:
        couleur (str): La couleur du joueur qui commence ('yellow' pour les jaunes, 'red' pour les rouges).

    """
    if couleur == 'yellow':
        message.config(text="Les jaunes commencent")
    elif couleur == 'red':
        message.config(text="Les rouges commencent")

# fonction qui permet d'afficher le joueur actuel sur la fenetre tkinter, en modifiant le texte de label message
def affiche_joueur_fenetre(couleur):
    """
    Affiche le joueur actuel dans la fenêtre Tkinter.

    Args:
        couleur (str): La couleur du joueur actuel ('yellow' pour les jaunes, 'red' pour les rouges).

    """
    if couleur == 'yellow':
        message.config(text="Les jaunes jouent")
    elif couleur == 'red':
        message.config(text="Les rouges jouent")

# fonction qui permet d'afficher le gagnant sur la fenetre tkinter, en modifiant le texte de label message
def affiche_gagnant_fenetre(couleur):
    """
    Affiche le gagnant dans la fenêtre Tkinter.

    Args:
        couleur (str): La couleur du joueur gagnant ('yellow' pour les jaunes, 'red' pour les rouges).

    """
    if couleur == 'yellow':
        message.config(text="Les jaunes gagnent")
    elif couleur == 'red':
        message.config(text="Les rouges gagnent")

# fonction qui permet d'afficher le message "Aucun gagnant" dans le cas d'une parie nulle, en modifiant le texte de label message
def affiche_aucun_gagnant_fenetre():
    """
    Affiche qu'il n'y a pas de gagnant dans la fenêtre Tkinter.

    """
    message.config(text="Aucun gagnant")

# fonction qui permet d'afficher le score des joueurs, en modifiant le texte de label score
def affiche_victoires_fenetre(victoires):
    """
    Affiche le nombre de victoires dans la fenêtre Tkinter.

    Args:
        victoires (list): Une liste contenant trois entiers représentant respectivement le nombre de victoires des jaunes,
                          des rouges et le nombre de matchs nuls.

    """
    [jaunes, rouges, nulles] = victoires
    scoreJaunes.config(text="Jaunes : " + str(jaunes))
    scoreRouges.config(text= "Rouges : " + str(rouges))

# fonction qui permet d'effacer le texte de label message à la fin d'une partie, est donc appelée à la fin d'une partie
def efface_message_fenetre():
    """
    Efface le texte affiché dans le label message dans la fenêtre Tkinter.

    """
    message.config(text=" ")

# Cette fonction est utilisée pour préparer la fenêtre de jeu avant le début d'une nouvelle partie
# Elle efface les jetons de la grille et réinitialise le message affiché dans la fenêtre.
# la variable nbParties est utilisée pour adapter le comportement de la fonction initialise_fenetre()
def initialise_fenetre(nbParties):
    """
    Initialise la fenêtre de jeu.

    Cette fonction met à jour la fenêtre Tkinter pour refléter tous les changements effectués jusqu'à présent dans
    l'interface graphique, puis elle effectue une pause avant le début de la nouvelle partie.

    Args:
        nbParties (int): Le nombre de parties déjà jouées. Si 2, une pause plus longue est effectuée avant le début de la nouvelle partie.

    """
    TEMPS_PAUSE = 1
    fenetreJeu.update() # met à jour la fenêtre Tkinter pour refléter tous les changements effectués jusqu'à présent dans 
                        # l'interface graphique.
    # Pause en secondes
    time.sleep(TEMPS_PAUSE) # Cette instruction fait une pause de 1 seconde avant de continuer. Cela permet aux utilisateurs 
                            # de voir la mise à jour de la fenêtre avant le début de la nouvelle partie.
    if nbParties == 2:      # cela signifie que le joueur a déjà joué une ou plusieurs parties auparavant. Dans ce cas, la 
                            # fonction peut ajouter une pause plus longue avant le début de la nouvelle partie. Cela peut être 
                            # utile si le joueur souhaite prendre une capture d'écran de la fenêtre.
                            # Si nbParties est égal à 1, cela signifie que le joueur vient de commencer une nouvelle session de 
                            # jeu et aucune partie n'a encore été jouée. Dans ce cas, la fonction peut simplement initialiser 
                            # la fenêtre pour la première partie sans nécessiter une pause prolongée.
        time.sleep(TEMPS_PAUSE*9) # Si nbParties==2, cela fait une pause de 9 secondes. Cela semble être une pause plus longue 
                                  # pour permettre à l'utilisateur de prendre une capture d'écran.
    # Dans la fenêtre graphique
    destruction_jetons()
    efface_message_fenetre()
    fenetreJeu.update()
    # Pause en secondes
    time.sleep(TEMPS_PAUSE)

# Utiliser la fonction random pour choisir au hasard le joueur qui commence une partie
couleurJoueur = rd.choice(['yellow', 'red'])
affiche_joueur_qui_commence_fenetre(couleurJoueur)

def reinitialiser_fenetre():
    """
    Réinitialise la grille de jeu dans la fenêtre graphique en effaçant tous les jetons.
    """
    global finPartie
    global listePositions
    global couleurJoueur
    global victoires
    global blocageJoueur
    # Réinitialisation des variables globales
    finPartie = False
    listePositions = initialise_liste_jetons()
    couleurJoueur = rd.choice(['yellow', 'red'])
    victoires = [0] * 3
    blocageJoueur = False
    # Effacer tous les jetons de la grille dans la fenêtre graphique
    destruction_jetons()
    # Afficher le joueur qui commence dans le terminal et dans la fenêtre graphique
    affiche_joueur_qui_commence_terminal(couleurJoueur)
    affiche_joueur_qui_commence_fenetre(couleurJoueur)
    [jaunes, rouges, nulles] = victoires
    scoreJaunes.config(text="Jaunes : " + str(jaunes))
    scoreRouges.config(text= "Rouges : " + str(rouges))
boutton_jouer.config(command=reinitialiser_fenetre)


# IMPLEMENTER UNE ANIMATION 
cpt1 = 0
def dessine_efface1():
    """
    Alterne entre le dessin et l'effacement d'un cercle sur le canevas2.

    Cette fonction dessine un cercle rose sur le canevas2 si le compteur `cpt1` est à 0, sinon elle efface le cercle
    existant. Elle alterne entre dessin et effacement à intervalles réguliers.

    """
    global cpt1, cercle1
    cpt1 = 1 - cpt1 # vaut alternativement 0 et 1
    if cpt1 == 0:
        cercle1 = canvas2.create_oval((0, 0), (50, 50), fill="pink4", width=0) 
    else:
        canvas2.delete(cercle1)
    canvas2.after(1000, dessine_efface1)
canvas2 = tk.Canvas(fenetreJeu, bg="dark slate gray",height=50, width=50, highlightthickness=0) # highlightthickness = 0 sert à
                                                                                                # supprimer les bords blancs du
                                                                                                # canvas.
canvas2.grid(column=0, row=0)
cercle1 = canvas2.create_oval((0, 0), (50, 50), fill="pink4", width=0) 
dessine_efface1()

cpt2 = 0
def dessine_efface2():
    """
    Alterne entre le dessin et l'effacement d'un cercle sur le canevas3.

    Cette fonction dessine un cercle rose sur le canevas3 si le compteur `cpt2` est à 0, sinon elle efface le cercle
    existant. Elle alterne entre dessin et effacement à intervalles réguliers.

    """
    global cpt2, cercle2
    cpt2 = 1 - cpt2 # vaut alternativement 0 et 1
    if cpt2 == 0:
        cercle2 = canvas3.create_oval((0, 0), (50, 50), fill="pink4", width=0) 
    else:
        canvas3.delete(cercle2)
    canvas3.after(1000, dessine_efface2)
canvas3 = tk.Canvas(fenetreJeu, bg="dark slate gray", height=50, width=50, highlightthickness=0)
canvas3.grid(column=2, row=0)
cercle2 = canvas3.create_oval((0, 0), (50, 50), fill="pink4", width=0) 
dessine_efface2()

def affiche_grille_terminal(jetons):
    """
    Affiche la grille de jeu dans le terminal en formatant les jetons selon une disposition de grille.
    Args:
        jetons (list): Une liste contenant les symboles des jetons pour chaque position de la grille.
                       La taille de la liste doit correspondre à NB_COLONNES * NB_LIGNES.
    Les constantes NB_COLONNES et NB_LIGNES doivent être définies dans le scope global du script pour que cette
    fonction fonctionne correctement.
    """
    i = NB_COLONNES*(NB_LIGNES-1)
    while i >= 0:
        print(jetons[i:i+NB_COLONNES])
        i = i - NB_COLONNES

    print()
#Cette fonction prend en entrée une liste `jetons` qui contient les symboles (par exemple, 'R', 'J', ou ' ')
#représentant l'état actuel de chaque position dans une grille de jeu structurée avec des lignes et des colonnes.
#Elle affiche cette liste sous la forme d'une grille dans le terminal, avec les positions de jetons disposées de bas en
#haut et de gauche à droite selon les constantes NB_COLONNES et NB_LIGNES définissant la taille de la grille.
#La grille est affichée en commençant par la dernière ligne et en remontant vers la première ligne.



def affiche_joueur_qui_commence_terminal(couleur):
    """
    Affiche dans le terminal le joueur qui commencera la partie, selon la couleur spécifiée.
    Args:
        couleur (str): La couleur du joueur qui doit commencer. Les valeurs attendues sont 'yellow' ou 'red'.
        Si une couleur différente de 'yellow' ou 'red' est passée en argument, aucun message spécifique n'est affiché.
        Cette fonction pourrait être étendue pour gérer des cas d'erreur ou des valeurs inattendues de manière plus robuste.
    """
    if couleur == 'yellow':
        print('Les jaunes commencent')
    elif couleur == 'red':
        print('Les rouges commencent')

#Cette fonction annonce dans le terminal quel joueur commence la partie en se basant sur la couleur fournie en argument.
#Elle accepte deux valeurs pour la couleur : 'yellow' pour les jaunes et 'red' pour les rouges. Selon la couleur passée,
#la fonction affiche un message approprié.



def affiche_joueur_terminal(couleur):
    """
    Affiche dans le terminal le joueur actuel selon la couleur spécifiée.
    Args:
        couleur (str): La couleur du joueur qui est en train de jouer. Accepte 'yellow' pour les jaunes et 'red' pour les rouges.
    Cette fonction annonce dans le terminal quel joueur est en train de jouer. Elle vérifie la couleur passée en argument
    et affiche un message approprié en fonction de cette couleur.
    """
    if couleur == 'yellow':
        print('Les jaunes jouent')
    elif couleur == 'red':
        print('Les rouges jouent')

#Si la couleur est 'yellow', affiche 'Les jaunes ont gagné'.
#Si la couleur est 'red', affiche 'Les rouges ont gagné'.
    

def affiche_gagnant_terminal(couleur):
    """
    Affiche dans le terminal le joueur gagnant selon la couleur spécifiée.
    Args:
        couleur (str): La couleur du joueur qui a gagné la partie. Doit être 'yellow' ou 'red'.
    Cette fonction annonce le gagnant de la partie en fonction de la couleur fournie. Elle affiche un message
    indiquant le joueur qui a remporté la partie sans passer à la ligne suivante grâce à l'utilisation de `end=''`.
    """
    if couleur == 'yellow':
        print('Les jaunes ont gagné', end='')
    elif couleur == 'red':
        print('Les rouges ont gagné', end='')

#Si la couleur est 'yellow', affiche 'Les jaunes ont gagné'.
#Si la couleur est 'red', affiche 'Les rouges ont gagné'


def affiche_aucun_gagnant_terminal():
    """
    Affiche un message indiquant qu'aucun joueur n'a gagné la partie (match nul).
    Cette fonction est utilisée pour annoncer un résultat de match nul dans le terminal. Elle affiche le message 'Match nul!'
    lorsqu'aucun des joueurs n'a réussi à remporter la partie.
    """
    print('Match nul!')




def affiche_score_terminal(victoires):
    """
    Affiche les scores des joueurs dans le terminal.
    Args:
        victoires (list): Liste contenant le nombre de victoires des jaunes, des rouges et le nombre de parties nulles,
                          typiquement sous la forme [jaunes, rouges, nulles].
    Cette fonction affiche le score actuel pour les joueurs jaunes et rouges ainsi que le nombre de parties nulles.
    Elle décompose la liste `victoires` en trois catégories distinctes et affiche ces informations de manière claire.
    """
    [jaunes, rouges, nulles] = victoires
    print('Jaunes : ' + str(jaunes))  # score des jaunes
    print('Rouges : ' + str(rouges))  # score des rouges
    print('Nulles : ' + str(nulles))  # Parties nulles
    print()


def initialise_liste_jetons():
    """
    Initialise la liste des jetons pour représenter une grille de jeu vide.
    Returns:
        list: Une liste de zéros représentant une grille de jeu vide, où chaque zéro indique une case non occupée.
              La taille de la liste est déterminée par NB_COLONNES * NB_LIGNES.
    """
    return [0] * (NB_COLONNES * NB_LIGNES)



def alignement(somme, nbPions, couleur):
    """
    Détermine si un alignement de pions correspondant à une couleur spécifique est atteint.
    Args:
        somme (int): La somme des valeurs dans un segment de la grille à vérifier.
        nbPions (int): Le nombre de pions à aligner pour gagner.
        couleur (str): La couleur du joueur ('yellow' pour jaune ou 'red' pour rouge).
    Retourne:
        un booleen: Vrai si un alignement correspondant à la couleur spécifiée est atteint, sinon faux.
    """
    pionsAlignes = False
    if (couleur == 'yellow' and somme == nbPions) or (couleur == 'red' and somme == -nbPions):
        pionsAlignes = True
    return pionsAlignes
#Cette fonction analyse la somme des valeurs d'un segment de la grille pour déterminer si elle correspond à un alignement complet
#de pions pour un joueur spécifique. Un alignement pour les jaunes est vérifié si la somme est égale à `nbPions` et pour les rouges si
#la somme est égale à `-nbPions`.



def alignements_pleins(jetons, nbPions, couleur):
    """
    Identifie et retourne les alignements complets de pions pour une couleur donnée.
    Args:
        jetons (list): Liste représentant la grille de jeu avec des valeurs associées à chaque case (par exemple, 1 pour jaune, -1 pour rouge, 0 pour vide).
        nbPions (int): Nombre de pions consécutifs nécessaires pour constituer un alignement valide.
        couleur (str): Couleur des pions à vérifier ('yellow' pour les jaunes, 'red' pour les rouges).

    Retourne:
        list: Liste des alignements trouvés. Chaque alignement est représenté par une liste contenant la colonne de départ (1-indexé), la ligne de départ (1-indexé),
              et la direction de l'alignement ('H' pour horizontal, 'V' pour vertical, 'DM' pour diagonale montante, 'DD' pour diagonale descendante).
              Si des alignements sont trouvés, le nombre de pions alignés est préfixé à la liste.

    La fonction parcourt la grille de jeu et vérifie les alignements possibles dans toutes les directions :
    horizontale, verticale, diagonale montante et diagonale descendante. Elle utilise la fonction `alignement` pour vérifier
    si un groupe de cases correspond à un alignement valide selon la couleur spécifiée et le nombre de pions.
    """
    listeAlignementsPleins = []
    # Vérification des alignements horizontaux
    for j in range(NB_LIGNES):
        for i in range(NB_COLONNES-nbPions+1):
            somme = 0
            for k in range(nbPions):
                somme += jetons[NB_COLONNES*j+i+k]
            if alignement(somme, nbPions, couleur):
                listeAlignementsPleins += [i+1,j+1,"Horizontal"]
    # Vérification des alignements verticaux
    for j in range(NB_LIGNES-nbPions+1):
        for i in range(NB_COLONNES):
            somme = 0
            for k in range(nbPions):
                somme += jetons[NB_COLONNES*j+i+k*NB_COLONNES]
            if alignement(somme, nbPions, couleur):
                listeAlignementsPleins += [i+1,j+1,"Vertical"]
    # Vérification des diagonales montantes
    for j in range(NB_LIGNES-nbPions+1):
        for i in range(NB_COLONNES-nbPions+1):
            somme = 0
            for k in range(nbPions):
                somme += jetons[NB_COLONNES*j+i+k*NB_COLONNES+k]
            if alignement(somme, nbPions, couleur):
                listeAlignementsPleins += [i+1,j+1,"DiagonaleMontante"]
    # Vérification des diagonales descendantes
    for j in range(nbPions-1, NB_LIGNES):
        for i in range(NB_COLONNES-nbPions+1):
            somme = 0
            for k in range(nbPions):
                somme += jetons[NB_COLONNES*j+i-k*NB_COLONNES+k]
            if alignement(somme, nbPions, couleur):
                listeAlignementsPleins += [i+1,j+1,"DiagonalDescandante"]
    if listeAlignementsPleins != []:
        listeAlignementsPleins = [nbPions] + listeAlignementsPleins
    return listeAlignementsPleins



def grille_pleine(jetons):
    """
    Détermine si la grille de jeu est totalement remplie.

    Cette fonction parcourt chaque case de la grille de jeu pour vérifier s'il reste des cases vides.
    Une case vide est représentée par la valeur 0 dans la liste des jetons.
    Args:
        jetons (list): Une liste d'entiers représentant l'état de la grille de jeu. 
                       Les valeurs sont 1 ou -1 pour les pions joués, et 0 pour les cases vides.
    Returns:
        bool: Retourne True si la grille est pleine, False autrement.
    """
    plein = True
    for i in range(NB_LIGNES*NB_COLONNES):
        if jetons[i] == 0:
            plein = False
    return plein



def inverse(couleur):
    """ Inverse les couleurs"""
    if couleur == 'yellow':
        couleur = 'red'
    elif couleur == 'red':
        couleur = 'yellow'
    return couleur



def colonne_pleine(jetons, colonne):
    """Vérifie si la colonne spécifiée est pleine dans la grille de jeu.

    Args:
        jetons (list): Liste représentant l'état actuel de la grille de jeu.
        colonne (int): Numéro de colonne (1-indexé) à vérifier.
    Returns:
        bool: True si la colonne est pleine, False sinon.
    """
    plein = True
    position = NB_COLONNES*(NB_LIGNES-1)+colonne-1
    if jetons[position] == 0:
        plein = False
    return plein
#Cette fonction prend en entrée la liste `jetons` représentant l'état de la grille de jeu et le numéro de colonne
#à vérifier. Elle retourne True si la colonne est pleine, c'est-à-dire si la case la plus basse dans la colonne
#est déjà occupée par un pion. Sinon, elle retourne False, indiquant qu'il reste au moins une case vide dans la colonne.
    


def jouer(jetons, couleur, colonne):
    """
    Moteur du jeu qui place un pion de la couleur spécifiée dans la colonne indiquée.

    Args:
        jetons (list): Liste représentant l'état actuel de la grille de jeu.
        couleur (str): Couleur du joueur ('yellow' pour jaune ou 'red' pour rouge).
        colonne (int): Numéro de colonne (1-indexé) dans laquelle placer le pion.

    Returns:
        list: Liste mise à jour représentant l'état de la grille après avoir placé le pion.
    """
    if not colonne_pleine(jetons, colonne):
        # On remplit la liste des jetons
        position = colonne - 1
        ligneSupport = 0
        while jetons[position]:
            ligneSupport += 1
            position += NB_COLONNES
        if couleur == 'yellow':
            valeur = 1
        elif couleur == 'red':
            valeur = -1            
        jetons[position] = valeur
    # On affiche la grille pour visualiser les jetons
    affiche_grille_terminal(jetons)                                   # Affichage Grille
    if MODE_GRAPHIQUE:
        affiche_grille_fenetre(colonne, ligneSupport, couleur)
    return jetons

#Cette fonction prend en entrée la liste `jetons` représentant l'état actuel de la grille de jeu,
#la couleur du joueur qui place le pion, et le numéro de colonne dans laquelle placer le pion.
#Si la colonne spécifiée n'est pas pleine, la fonction place le pion dans la colonne au niveau de la
#position la plus basse disponible. Elle met à jour la liste `jetons` avec le nouveau placement du pion
#et retourne la grille mise à jour.

#La fonction affiche également la grille de jeu dans le terminal et, si le mode graphique est activé,
#affiche également le pion dans la fenêtre graphique du jeu.


def fin_partie(jetons, couleur, victoires):
    """
    Vérifie si la partie est terminée et met à jour les scores en conséquence.

    Args:
        jetons (list): Liste représentant l'état actuel de la grille de jeu.
        couleur (str): Couleur du joueur actuel ('yellow' pour jaune ou 'red' pour rouge).
        victoires (list): Liste contenant le nombre de victoires des jaunes, des rouges et le nombre de parties nulles,
                          typiquement sous la forme [jaunes, rouges, nulles].

    Returns:
        tuple: Un tuple contenant trois éléments :
               - fin (bool): True si la partie est terminée, False sinon.
               - couleur (str): Couleur du prochain joueur si la partie n'est pas terminée.
               - victoires (list): Liste mise à jour des scores après la fin de la partie.
    """
    [jaunes, rouges, nulles] = victoires
    # On teste si la partie est finie
    fin = False
    if alignements_pleins(jetons, ALIGNEMENT, couleur):
        fin = True
        if couleur == 'yellow':
            jaunes += 1
        elif couleur == 'red':
            rouges += 1
        # On affiche le gagnant
        affiche_gagnant_terminal(couleur)
        nbCoups = analyse_victoire(jetons)
        print(" en", nbCoups, "coups")
        if MODE_GRAPHIQUE:
            affiche_gagnant_fenetre(couleur)
    elif grille_pleine(jetons):
        fin = True
        nulles += 1
        # On affiche aucun gagnant
        affiche_aucun_gagnant_terminal()
        if MODE_GRAPHIQUE:
            affiche_aucun_gagnant_fenetre()
    else:
        couleur = inverse(couleur)
        # On affiche qui doit jouer
        affiche_joueur_terminal(couleur)
        if MODE_GRAPHIQUE:
            affiche_joueur_fenetre(couleur)
    victoires = [jaunes, rouges, nulles]
    return fin, couleur, victoires

#Cette fonction vérifie si la partie est terminée en vérifiant s'il y a un alignement complet de pions ou si la grille
#est complètement remplie. Si la partie est terminée, elle met à jour les scores en fonction du résultat (victoire d'un
#joueur ou match nul) et affiche le résultat dans le terminal. Si la partie n'est pas terminée, elle détermine la couleur
#du prochain joueur et l'affiche dans le terminal.

#La fonction retourne un tuple contenant un booléen indiquant si la partie est terminée, la couleur du prochain joueur
#si la partie n'est pas terminée, et la liste mise à jour des scores.

def analyse_victoire(positions):
    """Analyse la victoire"""
    # Nombre de coups du gagnant
    nbPositionsPleines = NB_LIGNES*NB_COLONNES
    for i in range(NB_LIGNES*NB_COLONNES):
        if positions[i] == 0:
            nbPositionsPleines -= 1
    return math.ceil(nbPositionsPleines/2)  ## Arrondi à l'entier supérieur

#Cette fonction analyse l'état actuel de la grille de jeu et détermine le nombre de coups qui ont été joués jusqu'à présent.
#Le nombre de coups est calculé en comptant le nombre total de cases remplies dans la grille. Le nombre total de cases est
#déterminé par le produit du nombre de lignes et de colonnes de la grille (NB_LIGNES * NB_COLONNES). Le nombre de coups
#est ensuite calculé en soustrayant le nombre de cases vides de ce total, puis en divisant le résultat par 2 pour obtenir
#le nombre de coups joués par chaque joueur.

# Variables globales
finPartie = True
listePositions = []
couleurJoueur = ''
victoires = [0] * 3  # Jaunes, Rouges, Nulles
blocageJoueur = False


def mouse_clic(event):
    """
    Gestion du clic de souris dans la fenêtre du jeu Puissance 4.

    Args:
        event: L'événement de clic de souris Tkinter.

    Cette fonction gère les actions à effectuer lorsque l'utilisateur clique dans la fenêtre du jeu.
    Si la partie est terminée, elle réinitialise la grille de jeu et détermine aléatoirement la couleur du joueur qui commence.
    Si la partie est en cours, elle détermine la colonne dans laquelle l'utilisateur a cliqué et vérifie si cette colonne est valide.
    Si c'est le cas, elle met à jour la grille avec le jeton du joueur actuel et vérifie si la partie est terminée.
    Si la partie est terminée, elle affiche le bilan de la partie.
    """
    global finPartie
    global listePositions
    global couleurJoueur
    global victoires
    global blocageJoueur  # Indispensable pour les cas où l'on clique trop vite
    if not blocageJoueur:
        if finPartie:
            blocageJoueur = True
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
            blocageJoueur = False
        else:
            x = event.x
            colonne = col = 0
            while col < NB_COLONNES:
                col = col + 1
                ray = rayon()
                if x > col*ESPACEMENT+2*(col-1)*ray and x < col*ESPACEMENT+2*col*ray:
                    colonne = col
            if (colonne and not colonne_pleine(listePositions, colonne)):
                blocageJoueur = True
                listePositions = jouer(listePositions, couleurJoueur, colonne)
                finPartie, couleurJoueur, victoires = fin_partie(listePositions, couleurJoueur, victoires)  # Teste si la partie est finie
                if finPartie:
                    # Bilan
                    affiche_gagnant_terminal(victoires)  # Jaunes, Rouges, Nulles
                    affiche_victoires_fenetre(victoires)  # Jaunes, Rouges, Nulles
                blocageJoueur = False

# La méthode bind() permet de lier un évènement avec une fonction
grille.bind('<Button-1>', mouse_clic)

finPartie = False
listePositions = initialise_liste_jetons()
couleurJoueur = rd.choice(['yellow', 'red'])
affiche_joueur_qui_commence_terminal(couleurJoueur)
affiche_joueur_qui_commence_fenetre(couleurJoueur)


# Fonction pour sauvegarder une partie
def sauvegarder_partie(jetons, couleur, victoires):
    """
    Sauvegarde l'état actuel de la partie dans un fichier JSON.
    Args:
        jetons (list): Liste représentant l'état actuel de la grille de jeu.
        couleur (str): Couleur du joueur actuel ('yellow' pour jaune ou 'red' pour rouge).
        victoires (list): Liste contenant le nombre de victoires des jaunes, des rouges et le nombre de parties nulles.
    """
    partie = {
        "jetons": jetons,
        "couleur": couleur,
        "victoires": victoires
    }
    with open("partie_sauvegardee.json", "w") as f:
        json.dump(partie, f)

# Fonction pour charger une partie sauvegardée
def charger_partie():
    """
    Charge l'état d'une partie sauvegardée depuis un fichier JSON.
    Returns:
        dict: Un dictionnaire contenant l'état de la partie chargée.
    """
    try:
        with open("partie_sauvegardee.json", "r") as f:
            partie = json.load(f)
        return partie
    except FileNotFoundError:
        print("Aucune partie sauvegardée trouvée.")
        return None
boutton_sauvegarder_une_partie.config(command=lambda : sauvegarder_partie(listePositions, couleurJoueur, victoires))
#boutton_charger_une_partie.config(command=charger_partie)

# Pour sauvegarder une partie
# sauvegarder_partie(listePositions, couleurJoueur, victoires)

# Pour charger une partie sauvegardée
# partie_chargee = charger_partie()
# if partie_chargee:
#     listePositions = partie_chargee["jetons"]
#     couleurJoueur = partie_chargee["couleur"]
#     victoires = partie_chargee["victoires"]

# CREATION DE LA BOUCLE PRINCIPALE 
fenetreJeu.mainloop()