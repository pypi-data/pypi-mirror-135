import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm

n_clusters = 4
max_iter = 100
rseed = 5
row_norm = ""
X = [1,2,3,4,5,6]
centers = []

def initialize_center(X, n_clusters, rseed):
    rng = np.random.RandomState(rseed)
    i = rng.permutation(np.shape(X)[0])[:n_clusters]
    for k in range(n_clusters):
        np.append(centers[k],i)
    return centers


def add_records(X, labels,n_clusters):
    centroids = np.zeros((n_clusters,np.shape(X)[1]))
    for k in range(n_clusters):
       centroids[k, :] = np.mean(X[labels == k, :], axis = 0)
    return centroids


def find_distance(X, centroids,n_clusters):
    distance = np.zeros((np.shape(X)[0], n_clusters))
    for k in range(n_clusters):
        row_norm = norm(X - centroids[k])
        distance[:, k] = np.square(row_norm)
    return distance


def find_closest_cluster(distance):
    return np.argmin(distance, axis = 1)


def compute_sse(X, labels, centroids, n_clusters):
    distance = np.zeros(np.shape(X)[0])
    for k in n_clusters:
        distance[labels == k] = norm(X[labels == k] - centroids[k], axis = 1)
    return np.sum(np.square(distance))


def fit(X, max_iter, labels, n_clusters):
    centroids = initialize_center(X,n_clusters,rseed)
    for i in range(max_iter):
        old_centroids = centroids
        distance = find_distance(X, old_centroids, n_clusters)
        labels = find_closest_cluster(distance)
        centroids = add_records(X, labels, n_clusters)
        if np.all(old_centroids == centroids):
            plt.scatter(centroids[ :, 0], centroids[ :, 1])
            plt.show()
            break

