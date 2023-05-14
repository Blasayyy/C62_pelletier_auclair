import re
import numpy as np
class Entrainement():
    def __init__(self, chemin: str, enc: str, tfen: int) -> None:
        self.chemin, self.enc, self.tfen = chemin, enc, tfen

    @property
    def vocabulaire(self) -> dict:
        return self.__d

    @property
    def matrice(self) -> np.array:
        return self.__m

    def parser_texte(self):
        with open(self.chemin, encoding = self.enc) as f:
            self.__texte = re.findall('\w+', f.read().lower())

    def entrainer(self) -> None:
        self.parser_texte()
        self.creer_vocabulaire()
        self.indexer_texte()
        self.creer_matrice()
        self.extraire_cooccurrences()

    def creer_vocabulaire(self):
        self.__d = {}

    def creer_matrice(self):
        self.__m =  np.zeros((len(self.__d), len(self.__d)))

    def indexer_texte(self) -> None:
        for mot in self.__texte:
            if mot not in self.__d:
                self.__d[mot] = len(self.__d)

    def extraire_cooccurrences(self) -> None:
        for i in range(len(self.__texte)):
            for j in range(1, self.tfen//2 + 1):
                if i-j >= 0:
                    self.__m[self.__d[self.__texte[i]], self.__d[self.__texte[i-j]]] += 1
                if i+j < len(self.__texte):
                    self.__m[self.__d[self.__texte[i]], self.__d[self.__texte[i+j]]] += 1


