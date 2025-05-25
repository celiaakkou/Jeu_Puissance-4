# Jeu_Puissance-4
Description du projet
Ce projet est une implémentation du jeu classique Puissance 4 en Python utilisant la bibliothèque Tkinter pour l'interface graphique. Le jeu oppose deux joueurs qui alternent pour placer des jetons de leur couleur dans une grille verticale de 6 lignes et 7 colonnes. Le but est d'aligner 4 jetons de sa couleur horizontalement, verticalement ou en diagonale avant son adversaire.

Fonctionnalités principales
Interface graphique intuitive avec animation des jetons qui tombent

Mode console pour suivre le déroulement du jeu

Système de score qui compte les victoires de chaque joueur et les matchs nuls

Sauvegarde/chargement des parties en cours

Personnalisation des paramètres visuels (vitesse de chute, taille de la grille)

Animation visuelle avec des indicateurs clignotants

Configuration requise
Python 3.x

Bibliothèques Python:

tkinter

random

time

json

math

Installation
Téléchargez tous les fichiers du projet

Assurez-vous que Python 3 est installé sur votre système

Les bibliothèques requises sont incluses dans la distribution standard de Python

Comment jouer
Lancez le programme avec python puissance4.py

Cliquez sur la colonne où vous souhaitez placer votre jeton

Le jeu alterne automatiquement entre les joueurs jaune et rouge

Le premier à aligner 4 jetons gagne la partie

Utilisez les boutons pour:

Rejouer (réinitialise la partie)

Sauvegarder (enregistre la partie en cours)

Quitter (ferme l'application)

Personnalisation
Vous pouvez modifier les paramètres au début du fichier:

NB_PARTIES: Nombre de parties à jouer

MODE_GRAPHIQUE: Active/désactive l'interface graphique

TEMPS_CHUTE: Vitesse d'animation des jetons

LARGEUR_GRILLE: Taille de la grille de jeu

NB_COLONNES/NB_LIGNES: Dimensions de la grille

ALIGNEMENT: Nombre de jetons à aligner pour gagner

Structure du code
Le code est organisé en plusieurs sections:

Configuration initiale - Paramètres globaux du jeu

Interface graphique - Création des widgets Tkinter

Fonctions de jeu - Logique du Puissance 4

Fonctions d'affichage - Pour la console et l'interface

Gestion des événements - Interactions utilisateur

Sauvegarde/chargement - Persistance des parties

Auteurs
AKKOU Celia 

Licence
L2 Informatique - Université de Versaille Saint Quentin 
