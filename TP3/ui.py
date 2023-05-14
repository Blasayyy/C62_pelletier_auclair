from recherche import Recherche
from time import time

QUITTER = 'q'
MESS = f'''
Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul,
i.e. produit scalaire: 0, least-squares: 1, city-block: 2

Tapez {QUITTER} pour quitter.

'''

def demander(chercheur: Recherche, verbose: bool = False) -> None:
    reponse = input(MESS)
    while reponse != QUITTER:
        try:
            mot, nb, methode = reponse.split()
            print()
            t = time()
            for _score, _mot in chercheur.chercher(mot, int(nb), int(methode)):
                print(f'{_mot} -> {_score}')
            if verbose:
                print(f'\nRecherche en {time()-t} secondes.\n')
        except ValueError:
            print('--> Veuillez respecter le format des arguments')
        except Exception as e:
            print(e)
        reponse = input(MESS)