from random import randint

class grille:
    
    def creation_grille(self, hauteur : int, largeur : int) -> list:
        """
        Crée un tableau constitué de x de largeur x et de longueur
        hauteur : entier représentant la hauteur en ligne du tableau
        largeur : entier représentant la largeur en colonne du tableau
        """
        grille = [[0 for x in range(largeur)] for y in range(hauteur)]
        return grille

    def placement_mine(self, grille : list, nombredemine : int, decouverte : list) -> list:
        """
        Place aléatoirement un nombre x de repère de mine dans le tableau précedemment créé
        grille : tableau precedemment créé
        nombredemine : entier représentant le nombre de mine à mettre dans le tableau
        decouverte : coordonnée de la première case découverte
        """
        mine = nombredemine
        while mine != 0:
            i, j = randint(0, len(grille) - 1), randint(0, len(grille[0]) - 1)
            if grille[i][j] != "X" and [j, i] != decouverte:
                grille[i][j] = "X"
                mine -= 1
        return grille
    
    def nb_mine_autour(self, grille : list) -> list:
        """
        Remplace les cases de la grille par un chiffre donnant le nombre de mine autour de lui
        grille : tableau precedemment créé et passé par la fonction placement_mine
        """
        for i in range(len(grille)):
            for j in range(len(grille[0])):
                if grille[i][j] != "X":
                    mine_autour = 0
                    for o in [-1, 0, 1]:
                        for k in [-1, 0, 1]:
                            no, nk = i + o, j + k
                            if 0 <= no < len(grille) and 0 <= nk < len(grille[0]) and grille[no][nk] == "X":
                                mine_autour += 1
                    grille[i][j] = mine_autour
        return grille