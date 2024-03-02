import pygame
import time

class Interface_graphique:
    
    def __init__(self):
        self.texture = pygame.image.load("carredemineur.png")
        self.compteurvide = pygame.image.load("compteurvide.png")
        self.boutonreset = pygame.image.load("boutonreset.png")
        self.logo = pygame.image.load("logo.png")
        self.son_intro = pygame.mixer.Sound("intro.mp3")
        
    def intro(self, screen, largeur, hauteur):
        """
        Fonction permettant d'afficher l'intro du jeu
        """
        self.son_intro.play()
        screen.fill((0, 0, 0))
        alpha = 0
        while alpha <= 255:
            self.logo.set_alpha(alpha)
            screen.fill((0, 0, 0))
            screen.blit(self.logo, (largeur // 2 - 45, hauteur // 2 - 45))
            pygame.display.flip()
            pygame.time.delay(5)
            alpha += 1
            
        pygame.time.delay(3000)
        
        while alpha >= 0:
            self.logo.set_alpha(alpha)
            screen.fill((0, 0, 0))
            screen.blit(self.logo, (largeur // 2 - 45, hauteur // 2 - 45))
            pygame.display.flip()
            pygame.time.delay(5)
            alpha -= 1
        
    def positionnementcarre(self, screen, largeur, hauteur):
        """
        Fonction permettant de placer les carrés représentant les cases de la grille
        
        screen : fenêtre du jeu
        largeur : entier représentant le nombre de cases en largeur dans la grille
        hauteur : entier représentant le nombre de cases en hauteur dans la grille
        """
        for i in range(largeur):
            for j in range(hauteur):
                screen.blit(self.texture, (i * 30+20, j * 30+100))
        
    def menu(self, screen, largeur):
        """
        Fonction permettant de placer les éléments du menu du jeu (compteur de mine, de temps et bouton reset)
        
        screen : fenêtre du jeu
        largeur : entier représensant la largeur de la fenêtre en pixel
        """
        screen.fill("grey")
        screen.blit(self.compteurvide, (30, 30))
        screen.blit(self.compteurvide, (largeur-110, 30))
        screen.blit(self.boutonreset, (largeur // 2 - 45, 5))
        

        
        
class Interface_interaction:
    
    def __init__(self, case_largeur, case_hauteur, nbdemine):
        self.casedecouverte = pygame.image.load("casedecouverte.png")
        self.mine = pygame.image.load("casemine.png")
        self.mineclique = pygame.image.load("casemineclique.png")
        self.mine_autour_police = pygame.font.Font("policechiffre.ttf", 20)
        self.rendu_texte_mine_autour = None
        self.compteur = pygame.font.Font("compteur.ttf", 55)
        self.rendu_texte_compteur = None
        self.rendu_texte_compteur_2 = None
        self.drapeau = pygame.image.load("drapeau.png")
        self.case_largeur = case_largeur
        self.case_hauteur = case_hauteur
        self.case_restante = case_largeur*case_hauteur - nbdemine
        self.debut = None
        self.actuel = None
        self.chronometre = 0
        self.partie_fini = False
        self.mine_restante = nbdemine
        self.gagne_image = pygame.image.load("gagne.png")
        self.perdu_image = pygame.image.load("perdu.png")
        self.son_perdu = pygame.mixer.Sound("explosion.mp3")
        self.son_perdu.set_volume(0.5)
        self.son_gagne = pygame.mixer.Sound("victoire.mp3")
        self.son_gagne.set_volume(0.5)
        self.graphisme_instance = Interface_graphique()


    def decouverte_case_vide(self, case_clique: list, grille: list, screen):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                ni, nj = case_clique[1] + i, case_clique[0] + j
                if 0 <= ni < len(grille) and 0 <= nj < len(grille[0]) and grille[ni][nj] == 0 or 0 <= ni < len(grille) and 0 <= nj < len(grille[0]) and grille[ni][nj] == 10:
                    grille[ni][nj] = "Show"
                    screen.blit(self.casedecouverte, (nj * 30 + 20, ni * 30 + 100))
                    self.case_restante -= 1
                    self.decouverte_case_vide([nj, ni], grille, screen)
                    for o in [-1, 0, 1]:
                        for k in [-1, 0, 1]:
                            no, nk = ni + o, nj + k
                            if 0 <= no < len(grille) and 0 <= nk < len(grille[0]) and grille[no][nk] != "Show":
                                screen.blit(self.casedecouverte, (nk*30+20, no*30+100))
                                self.rendu_texte_mine_autour = self.mine_autour_police.render(str(grille[no][nk]), True, (132, 1, 255))
                                screen.blit(self.rendu_texte_mine_autour, (nk*30+30, no*30+105))
                                grille[no][nk] = "Show"
                                self.case_restante -= 1
                                print(self.case_restante)

    def clic_gauche(self, grille, position, screen, largeur):
        case_clique = [(position[0]-20) // 30, (position[1]-100) // 30]
        print(case_clique)
        if 0 <= case_clique[0] < len(grille[0]) and 0 <= case_clique[1] < len(grille) and grille[case_clique[1]][case_clique[0]] != "Show":
            
            if grille[case_clique[1]][case_clique[0]] != "X" and grille[case_clique[1]][case_clique[0]] != "Bien" and grille[case_clique[1]][case_clique[0]] != 0 and grille[case_clique[1]][case_clique[0]] - 10 != 0:
                
                if grille[case_clique[1]][case_clique[0]] > 10:
                    grille[case_clique[1]][case_clique[0]] -= 10
                    
                screen.blit(self.casedecouverte, (case_clique[0]*30+20, case_clique[1]*30+100))
                self.rendu_texte_mine_autour = self.mine_autour_police.render(str(grille[case_clique[1]][case_clique[0]]), True, (132, 1, 255))
                screen.blit(self.rendu_texte_mine_autour, (case_clique[0]*30+30, case_clique[1]*30+105))
                grille[case_clique[1]][case_clique[0]] = "Show"
                self.case_restante -= 1
                print(self.case_restante)
                   
            elif grille[case_clique[1]][case_clique[0]] == "X" or grille[case_clique[1]][case_clique[0]] == "Bien":
                self.partie_fini = True
                screen.blit(self.perdu_image, (largeur // 2 - 45, 5))
                for i in range(0, len(grille)):
                    for j in range(0, len(grille[0])):
                        if grille[j][i] == "X":
                            screen.blit(self.mine, (i*30+20, j*30+100))
                        grille[j][i] = "Show"
                screen.blit(self.mineclique, (case_clique[0]*30+20, case_clique[1]*30+100))
                self.son_perdu.play()
            
            else:
                screen.blit(self.casedecouverte, (case_clique[0]*30+20, case_clique[1]*30+100))
                self.case_restante -= 1
                grille[case_clique[1]][case_clique[0]] = "Show"
                self.decouverte_case_vide(case_clique, grille, screen)
                print(self.case_restante)
                
                
        

    def clic_droit(self, grille, position, screen):
        case_clique = [(position[0]-20) // 30, (position[1]-100) // 30]
        print(case_clique)
        
        if 0 <= case_clique[0] < len(grille[0]) and 0 <= case_clique[1] < len(grille) and grille[case_clique[1]][case_clique[0]] == "X":
            print("Bombastic")
            screen.blit(self.drapeau, (case_clique[0]*30+20, case_clique[1]*30+100))
            grille[case_clique[1]][case_clique[0]] = "Bien"
            self.mine_restante -= 1
            
        elif 0 <= case_clique[0] < len(grille[0]) and 0 <= case_clique[1] < len(grille) and grille[case_clique[1]][case_clique[0]] == "Bien":
            print("BOOMbastic")
            screen.blit(self.graphisme_instance.texture, (case_clique[0]*30+20, case_clique[1]*30+100))
            grille[case_clique[1]][case_clique[0]] = "X"
            self.mine_restante += 1
        
        elif 0 <= case_clique[0] < len(grille[0]) and 0 <= case_clique[1] < len(grille) and grille[case_clique[1]][case_clique[0]] != "Show" and grille[case_clique[1]][case_clique[0]] < 10 :
            grille[case_clique[1]][case_clique[0]] += 10
            screen.blit(self.drapeau, (case_clique[0]*30+20, case_clique[1]*30+100))
            self.mine_restante -= 1
            print("Non")
            return
            
        elif 0 <= case_clique[0] < len(grille[0]) and 0 <= case_clique[1] < len(grille) and grille[case_clique[1]][case_clique[0]] != "Show" and grille[case_clique[1]][case_clique[0]] >= 10:
            print("OUI")
            screen.blit(self.graphisme_instance.texture, (case_clique[0]*30+20, case_clique[1]*30+100))
            grille[case_clique[1]][case_clique[0]] -= 10
            self.mine_restante += 1
            return
        
    def clic_molette(self, grille, screen, position, tour, largeur):
        if tour >= 1:
            case_clique = [(position[0]-20) // 30, (position[1]-100) // 30]
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    ni, nj = case_clique[1] + i, case_clique[0] + j
                    self.clic_gauche(grille, (nj* 30 + 20, ni* 30 + 100), screen, largeur)
            
            
    def cheatmode(self, grille, screen):
        for i in range(0, len(grille)):
            for j in range(0, len(grille[0])):
                if grille[j][i] == "X":
                    screen.blit(self.mine, (i*30+20, j*30+100))
                    
    def verification(self, grille, largeur, screen, tour):
        if self.case_restante == 0 and tour >= 0:
            for i in range(0, len(grille)):
                    for j in range(0, len(grille[0])):
                        grille[i][j] = "Show"
            self.partie_fini = True
            screen.blit(self.gagne_image, (largeur // 2 - 45, 5))
            self.son_gagne.play()

        
    def affichage_chronometre(self, screen, tour):
        """
        Fonction permettant d'afficher un chronometre
        
        screen : fenêtre où afficher le chronometre
        largeur : largeur de la fenêtre
        tour : nombre de tour écoulé
        """
        if tour == 1 and self.partie_fini == False:
            self.debut = time.time()
            self.actuel = time.time()
            tour += 1
        if tour > 1 and self.partie_fini == False and round(time.time()) != round(self.actuel):
            self.chronometre = round(self.actuel - self.debut)
            
            if self.chronometre < 10:
                self.chronometre = "00" + str(self.chronometre)
                
            if int(self.chronometre) < 100 and int(self.chronometre) >= 10:
                self.chronometre = "0" + str(self.chronometre)
            
            self.actuel = time.time()
        
        self.rendu_texte_compteur = self.compteur.render(str(self.chronometre), True, (255, 0, 0))
        screen.blit(self.graphisme_instance.compteurvide, (30, 30))
        screen.blit(self.rendu_texte_compteur, (33, 28))

    def affichage_mine_restante(self, screen, largeur):
        self.rendu_texte_compteur_2 = self.compteur.render(str(self.mine_restante), True, (255, 0, 0))
        screen.blit(self.graphisme_instance.compteurvide, (largeur-110, 30))
        screen.blit(self.rendu_texte_compteur_2, (largeur-110, 28))

