import numpy as np
from time import time


class KMeans:
    def __init__(self, n_clusters, max_iter=100, random_state=123):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state

    def initialize_centroids(self, data):
        np.random.RandomState(self.random_state)
        random_idx = np.random.permutation(data.shape[0])
        centroids = data[random_idx[:self.n_clusters]]
        return centroids

    def compute_centroids(self, data, labels):
        centroids = np.zeros((self.n_clusters, data.shape[1]))
        for k in range(self.n_clusters):
            centroids[k, :] = np.mean(data[labels == k, :], axis=0)
        return centroids

    def compute_distance(self, data, centroids):
        distance = np.zeros((data.shape[0], self.n_clusters))
        for k in range(self.n_clusters):
            row_norm = np.linalg.norm(data - centroids[k, :], axis=1)
            distance[:, k] = np.square(row_norm)
        return distance

    def find_closest_cluster(self, distance):
        return np.argmin(distance, axis=1)

    def compute_sse(self, data, labels, centroids):
        distance = np.zeros(data.shape[0])
        for k in range(self.n_clusters):
            distance[labels == k] = np.linalg.norm(data[labels == k, :] - centroids[k], axis=1)
        return np.sum(np.square(distance))

    def fit(self, data):
        self.centroids = self.initialize_centroids(data)
        for i in range(self.max_iter):
            start_time = time()
            old_centroids = self.centroids
            distance = self.compute_distance(data, old_centroids)
            old_labels = self.labels if hasattr(self, 'labels') else np.zeros(data.shape[0])
            self.labels = self.find_closest_cluster(distance)
            changes = np.sum(old_labels != self.labels)
            self.centroids = self.compute_centroids(data, self.labels)
            print(f'Iteration {i} completed in {time() - start_time} seconds ({changes} changes)')
            unique_labels, counts = np.unique(self.labels, return_counts=True)
            for label, count in zip(unique_labels, counts):
                print(f'There are {count} words belonging in centroid {label}')
            print('*'*63)
            if np.all(old_centroids == self.centroids):
                break
        self.error = self.compute_sse(data, self.labels, self.centroids)

    def predict(self, data):
        distance = self.compute_distance(data, self.centroids)
        return self.find_closest_cluster(distance)

