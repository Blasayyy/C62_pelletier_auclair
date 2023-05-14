from entrainementBD import EntrainementBD
from dao import DAO
from entrainement import Entrainement
import knn
import utils
from knn import KNN
from KMeans import KMeans
from KMeans2 import KMeans2

import entrainement
def main() -> int:
    with DAO() as bd:

        mots = bd.charger_mots()
        cooccurrences = bd.charger_cooccurrences(5)
        data, idx_to_word = utils.create_data_matrix(cooccurrences, mots)
        kmeans = KMeans2(n_clusters= 5)
        kmeans.fit(data)
        typed_words = utils.assign_word_types(mots, "Lexique382.tsv")
        knn = KNN(typed_words=typed_words)
        cluster_types, cluster_type_counts = knn.predict_cluster_type(kmeans.get_centroids(), data)

        utils.print_closest_words(kmeans.get_centroids(), data, typed_words, cluster_types, cluster_type_counts, 10)



if __name__ == '__main__':
    quit(main())