from sys import argv
import re

class Lecteur:
    def __init__(self, chemin, encodage):
        self.chemin = chemin
        self.encodage = encodage
        self.texte = None

    def __enter__(self):
        self.lire()
        return self

    def __exit__(self, exc_type, exc_val, exc_traceback):
        self.f.close()

    def lire(self):
        self.f = open(self.chemin, 'r', encoding=self.encodage)
        self.texte = self.f.read()


    def compter_caracteres(self):
        return len(re.findall('\w', self.texte))

    def compter_mots(self):
        return len(re.findall('\w+', self.texte))

    def compter_virgules(self):
        return self.texte.count(',')

    def compter_souschaine(self, souschaine):
        return len(re.findall(souschaine, self.texte))

    def afficher(self, souschaine):
        print(f'il y a {self.compter_caracteres()} caracteres')
        print(f'il y a {self.compter_mots()} mots')
        print(f'il y a {self.compter_virgules()} virgules')
        print(f'il y a {self.compter_souschaine(souschaine)} {souschaine}')

def main():
    chemin = "LesTroisMousquetairesUTF8.txt"
    enc = "utf-8"
    souschaine = "les"

    lecteur = Lecteur(chemin, enc)
    lecteur.lire()
    lecteur.afficher(souschaine)

    return 0

if __name__ == '__main__':
    quit(main())