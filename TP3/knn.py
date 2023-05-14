import numpy as np
from collections import Counter
from scipy.spatial import distance


class KNN:
    def __init__(self, typed_words):
        self.typed_words = typed_words


    def predict_cluster_type(self, centroids, data):
        cluster_types = []
        cluster_type_counts = []

        for centroid in centroids:
            dists = distance.cdist([centroid], data, 'euclidean')[0]

            closest_words = np.argsort(dists)

            type_counts = Counter()
            for i, word_idx in enumerate(closest_words, 1):
                _, _, word_type = self.typed_words[word_idx]
                type_counts[word_type] += 1 / i

            most_common_type = type_counts.most_common(1)[0][0]
            cluster_types.append(most_common_type)

            cluster_type_counts.append(type_counts[most_common_type])

        return cluster_types, cluster_type_counts


