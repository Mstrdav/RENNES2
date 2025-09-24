# 22503282 Colin Geindre

# Section 1 : les imports
import math
import numpy as np
import P01_utils as put
from scipy.spatial import KDTree

# Section 2 : les fonctions
def dist(x, y):
    """ Calcule la distance euclidienne entre deux points x et y."""
    return np.sqrt(np.sum((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2))

def speed_dist(x, y):
    """ Calcule la même chose mais sans prendre la racine carrée (car inutile, on va juste comparer des distances). """
    return np.sum((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

def find_k_nearest(x, X, k):
    """ Trouve les indices des k points les plus proches de x dans X."""
    distances = np.array([speed_dist(x, xi) for xi in X])
    return np.argsort(distances)[:k]

def majority(labels):
    """ Trouve la classe majoritaire dans une liste de labels."""
    values, counts = np.unique(labels, return_counts=True)
    return values[np.argmax(counts)]

def prediction(X, y, x, k=1):
    """ Prédit la classe de x en utilisant l'algorithme des k plus proches voisins."""
    indices = find_k_nearest(x, X, k)
    voisins_labels = [y[i] for i in indices]
    return majority(voisins_labels).tolist()

def k_plus_proches_voisins_liste(X, y, x_test, k=1):
    """ Prédit les classes des points de X_test en utilisant l'algorithme des k plus proches voisins."""
    return [prediction(X, y, x, k) for x in x_test]

# Section 3 : le code
# chargement des données
train = put.lire_donnees(100)
test = put.lire_donnees(10)
# put.visualiser_donnees(train[0], train[1], test[0])

# prédiction
k = 5
print(test[0])
y_pred = k_plus_proches_voisins_liste(train[0], train[1], test[0], k)
print("Prédictions :", y_pred)
print("Véritables classes :", test[1])

# Avec scipy
tree = KDTree(train[0]) # oui j'ai cherché sur Internet comment utiliser scipy
y_pred_scipy = []
for x in test[0]:
    dists, indices = tree.query(x, k=k)
    voisins_labels = [train[1][i] for i in indices]
    y_pred_scipy.append(majority(voisins_labels).tolist())

print("Prédictions avec scipy :", y_pred_scipy)