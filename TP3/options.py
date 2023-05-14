from sys import argv
from argparse import ArgumentParser
from codecs import lookup
from os.path import isfile
from traceback import print_exc

class Options():
    def __init__(self):
        self.creer_parseur()
        self.parser()

    def creer_parseur(self) -> None:
        self.p = ArgumentParser(description="Synonymes dans une BD")

        self.p.add_argument('-e', action="store_true", help="Entraînement")
        self.p.add_argument('-r', action="store_true", help="Recherche")
        self.p.add_argument('-b', action="store_true", help="Réinitialisation de la BD")
        self.p.add_argument('-c', action="store_true", help="Clustering")
        self.p.add_argument('-t', type=int, help="Taille de fenêtre")
        self.p.add_argument('-n', type=int, help="Nombre maximal de mots à afficher par cluster")
        self.p.add_argument('-k', type=int, help="Nombre de centroïdes")
        self.p.add_argument('--enc', type=str, help="Encodage du texte")
        self.p.add_argument('--chemin', type=str, help="Chemin du texte")
        self.p.add_argument('-v', action="store_true", help="Performance times")


    def parser(self) -> None:
        self.p.parse_args(args=argv[1:], namespace=Options)
        
        if self.e + self.r + self.b  + self.c!= 1:
            raise Exception("Vous devez choisir une et une seule option parmi -e, -r et -b")

        if self.e or self.r or self.c:
            if self.t is None or self.t < 1 or self.t % 2 != 1:
                raise Exception("S.V.P. entrez une taille de fenêtre positive et impaire")
            if self.c:
                if self.n is None or self.n < 1:
                    raise Exception("S.V.P. entrez un nombre maximal de mots à afficher par cluster")
                if self.k is None or self.k < 1:
                    raise Exception("S.V.P. entrez un nombre de centroïdes")
            if self.e:
                if self.enc is None:
                    raise Exception('S.V.P. fournir un encodage de fichier')
                lookup(self.enc)

                if self.chemin is None:
                    raise Exception("S.V.P. fournir un chemin de fichier")
                if not isfile(self.chemin):
                    raise Exception(f'"{self.chemin}" est un chemin invalide')

def main():
    try:
        opts = Options()
        print(opts.__dict__)
    except Exception as e:
        #print_exc()
        print(e)


    return 0

if __name__ == '__main__':
    quit(main())