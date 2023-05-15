from traceback import print_exc
from dao import DAO
from entrainementBD import EntrainementBD
from recherche import Recherche
from options import Options
from ui import demander
from time import time
from KMeans2 import KMeans2
from KMeans import KMeans
from knn import KNN
import utils

def main() -> int:
    try:
        options = Options()
        with DAO() as bd:
            if options.b:
                bd.creer_tables()
            elif options.c:
                cooccurrences = bd.charger_cooccurrences(options.t)
                mots = bd.charger_mots()
                data, idx_to_word = utils.create_data_matrix(cooccurrences, mots)

                #pour utiliser l'autre version du kmeans
                #model =  Kmeans(n_clusters= options.k)
                model = KMeans2(n_clusters= options.k)
                model.fit(data)

                typed_words = utils.assign_word_types(mots, "Lexique382.tsv")
                knn = KNN(typed_words=typed_words)
                cluster_types, cluster_type_counts = knn.predict_cluster_type(model.get_centroids(), data)

                utils.print_closest_words(model.get_centroids(), data, typed_words, cluster_types, cluster_type_counts,
                                          10)

            else:
                cerveau = EntrainementBD(options.chemin, options.enc, options.t, bd, options.v)
                if options.e:
                    t = time()
                    cerveau.entrainer()
                    if options.v:
                        print(f'\nEntraînement en {time()-t} secondes.\n')
                elif options.r:
                    cerveau.charger_donnees()
                    demander(Recherche(cerveau), options.v)

    except Exception as e:
        print(f'\n{e}\n')
        print_exc()
        return 1
    return 0

if __name__ == '__main__':
    quit(main())