import numpy as np

# fonction qui centre et réduit un ndarray
def centrer_reduire(X):
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    return (X - mean) / std

# tests
X = np.array([[1, 2, 3, 4, 5],[6, 7, 8, 9, 10]])
print(centrer_reduire(X))