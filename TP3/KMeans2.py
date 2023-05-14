from sklearn.cluster import MiniBatchKMeans
from time import time
import numpy as np


class KMeans2:
    def __init__(self, n_clusters, batch_size=100, max_iter=100, tol=0.0):
        self.n_clusters = n_clusters
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.tol = tol
        self.model = MiniBatchKMeans(n_clusters=n_clusters, batch_size=batch_size, max_iter=1, init_size=batch_size * 3)
        self.labels = None

    def fit(self, data):
        self.model.fit(data[:self.n_clusters])

        for i in range(self.max_iter):
            t = time()
            old_labels = self.labels
            self.model.partial_fit(data)
            self.labels = self.model.labels_
            changes = np.sum(old_labels != self.labels) if old_labels is not None else self.n_clusters
            print(f'Iteration {i} completed in {time() - t} seconds ({changes} changes)')
            self.print_cluster_info()

            if changes <= self.tol:
                print(f'Converged in {i} iterations')
                break

    def print_cluster_info(self):
        unique_labels, counts = np.unique(self.labels, return_counts=True)
        for label, count in zip(unique_labels, counts):
            print(f'There are {count} words belonging in centroid {label}')
        print('*' * 63)

    def get_centroids(self):
        return self.model.cluster_centers_
