from sklearn.cluster import KMeans
import numpy as np
import seaborn as sns

sns.set()
import pandas as pd

import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin

def initialize_center(X, n_clusters, rseed=5):
    np.random.RandomState(rseed)
    i = np.random.permutation(X.shape[0])
    centers = X[i[:n_clusters]]
return centers
########################################################################################################################
def add_records(X, labels):
    centroids = np.zeros((n_clusters, X.shape[1]))
    for k in range(n_clusters):
        centroids[k, :] = np.mean(X[labels == k, :], axis=0)

    return centroids
########################################################################################################################
def find_distance(X, centroids):
    distance = np.zeros((X.shape[0], n_clusters))
    for k in range(n_clusters):
        row_norm = norm(X - centroids[k, :], axis=1)
        distance[:, k] = np.square(row_norm)
    return distance
########################################################################################################################
def find_closest_cluster(distance):
    return np.argmin(distance, axis=1)
########################################################################################################################
def compute_sse(X, labels, centroids):
    distance = np.zeros(X.shape[0])
    for k in range(n_clusters):
        distance[labels == k] = norm(X[labels == k] - centroids[k], axis=1)
    return np.sum(np.square(distance))
########################################################################################################################
def fit(X):
    centroids = initialize_center(X)
    for i in range(max_iter):
        old_centroids = centroids
        distance = find_distance(X, old_centroids)
        labels = find_closest_cluster(distance)
        centroids = add_records(X, labels)
        if np.all(old_centroids == centroids):
            plt.scatter(old_centroids[:, 0], old_centroids[:, 1]);
        break

error = compute_sse(X, labels, centroids)
########################################################################################################################
def predict(X):
    distance = find_distance(X, old_centroids)
    return find_closest_cluster(distance)

