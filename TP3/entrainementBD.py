import numpy as np
from entrainement import Entrainement
from dao import DAO

#Ici, il y a du polymorphisme par redéfinition

class EntrainementBD(Entrainement):
    def __init__(self, chemin: str, enc: str, tfen: int, bd: DAO, v: bool) -> None:
        super().__init__(chemin, enc, tfen)
        self.bd = bd
        self.v = v
        
    def creer_vocabulaire(self) -> None:
        super().creer_vocabulaire()
        for mot, id in self.bd.charger_mots():
            self.vocabulaire[mot] = id

    def creer_matrice(self) -> None:
        super().creer_matrice()
        for r, c, freq in self.bd.charger_cooccurrences(self.tfen):
            self.matrice[r,c] = freq

    def entrainer(self) -> None:
        super().entrainer()
        if (self.v):
            print(self.matrice)
        self.maj()

    def maj(self) -> None:
        self.bd.inserer_mots(list(self.vocabulaire.items()))
        m0 = np.argwhere(self.matrice > 0)
        cooccs = [(int(r), int(c), self.tfen, self.matrice[r, c]) for r, c in m0]
        self.bd.inserer_cooccurrences(cooccs)
        
    def charger_donnees(self) -> None:
        self.creer_vocabulaire()
        self.creer_matrice()
