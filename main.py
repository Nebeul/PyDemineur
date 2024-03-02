import pygame
from donnee_grille import grille
from interface import *
import threading


class Jeu:
    def __init__(self):
        self.running = True
        self.largeur_case = 10
        self.hauteur_case = 10
        self.largeur = self.largeur_case*30+40
        self.hauteur = self.hauteur_case*30+120
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        self.nbdemine = 10
        self.grille_instance = grille()
        self.grille = None
        self.grille_finale = None
        self.interaction_instance = Interface_interaction(self.largeur_case, self.hauteur_case, self.nbdemine)
        self.graphisme_instance = Interface_graphique()
        self.tour = 0

    
    def creation_grille(self, longueur, largeur):
        self.grille = self.grille_instance.creation_grille(longueur, largeur)
        
    def ajout_mines(self, nbdemine, decouverte):
        self.grille_avec_mine = self.grille_instance.placement_mine(self.grille, nbdemine, decouverte)
        self.grille = self.grille_instance.nb_mine_autour(self.grille_avec_mine)
        
    def afficher_grille(self):
        print(self.grille)
        
    def reset_demineur(self):
        self.creation_grille(jeu.hauteur_case, jeu.largeur_case)
        self.graphisme_instance.menu(jeu.screen, jeu.largeur)
        self.graphisme_instance.positionnementcarre(jeu.screen, jeu.largeur_case, jeu.hauteur_case)
        self.tour = 0
        self.interaction_instance.chronometre = 0
        self.interaction_instance.mine_restante = self.nbdemine
        self.interaction_instance.case_restante = self.largeur_case*self.hauteur_case - self.nbdemine
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position_clic = pygame.mouse.get_pos()
                        print("Position du clic : x =", position_clic[0], ", y =", position_clic[1])
                        
                        if self.largeur // 2 - 45 <= position_clic[0] <= self.largeur // 2 + 45 and 5 <= position_clic[1] <= 95:
                            self.reset_demineur()
                        
                        if 20 < position_clic[0] < len(self.grille[0])*30 + 20 and 100 < position_clic[1] < len(self.grille)*30 + 100:    
                            self.tour += 1
                            print(self.tour)
                            
                        if self.tour == 1:
                            self.ajout_mines(jeu.nbdemine, [(position_clic[0]-20) // 30, (position_clic[1]-100) // 30])  # Ajout des mines à la grille
                            self.afficher_grille()  # Afficher la grille
                            self.interaction_instance.clic_gauche(self.grille, position_clic, self.screen, self.largeur)
                            jeu.interaction_instance.affichage_chronometre(jeu.screen, self.tour)
                            self.tour += 1

                        self.interaction_instance.clic_gauche(self.grille, position_clic, self.screen, self.largeur)
                        
                    if event.button == 2:
                        position_clic = pygame.mouse.get_pos()
                        self.interaction_instance.clic_molette(self.grille, self.screen, position_clic, self.tour, self.largeur)

                        
                    if event.button == 3:
                        position_clic = pygame.mouse.get_pos()
                        print("Position du clic : x =", position_clic[0], ", y =", position_clic[1])
                        self.interaction_instance.clic_droit(self.grille, position_clic, self.screen)
                
                elif event.type == pygame.KEYDOWN:
                    if event.mod & pygame.KMOD_LSHIFT:
                        self.interaction_instance.cheatmode(self.grille, self.screen)
                 
            self.interaction_instance.verification(self.grille, self.largeur, self.screen, self.tour)
            pygame.display.flip()
            jeu.interaction_instance.affichage_chronometre(jeu.screen, self.tour)
            jeu.interaction_instance.affichage_mine_restante(jeu.screen, jeu.largeur)
            

                    





pygame.init()
pygame.mixer.init()

jeu = Jeu()
jeu.graphisme_instance.intro(jeu.screen, jeu.largeur, jeu.hauteur)
pygame.time.wait(4000)
jeu.creation_grille(jeu.hauteur_case, jeu.largeur_case)
jeu.graphisme_instance.menu(jeu.screen, jeu.largeur)
jeu.graphisme_instance.positionnementcarre(jeu.screen, jeu.largeur_case, jeu.hauteur_case)
jeu.run()



pygame.quit()