import numpy as np
from entrainement import Entrainement

STOP = set('l le la les au aux un une du des c ça ce cette cet ces celle celui celles ceux je j tu il elle on nous vous ils elles me m te t se s y à de pour sans par mais ou et donc car ni or ne n pas dans que qui qu de d mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs lui en quel quelle quelles lequel laquelle lesquels lesquelles dont quoi quand où comment pourquoi sur dessus tout tous toutes avec comme avec'.split())

def scalar_product(u: np.array, v: np.array) -> float: return np.sum(u * v)
def least_squares(u: np.array, v: np.array) -> float: return np.sum((u - v) ** 2)
def city_block(u: np.array, v: np.array) -> float: return np.sum(np.abs(u - v))
F = [scalar_product, least_squares, city_block]

class Recherche:
    def __init__(self, cerveau: Entrainement) -> None:
        self.cerveau = cerveau

    def chercher(self, mot: str, nb: int, methode: int) -> list:
        if mot not in self.cerveau.vocabulaire:
            raise Exception(f'--> "{mot}" n\'est pas dans le vocabulaire')

        index = self.cerveau.vocabulaire[mot]
        vmot = self.cerveau.matrice[index]
        scores = []
        for _mot, _index in self.cerveau.vocabulaire.items():
            if _index != index and _mot not in STOP:
                scores.append( (F[methode](vmot, self.cerveau.matrice[_index]), _mot) )

        return sorted(scores, reverse = methode == 0)[:nb]
