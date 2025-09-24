# Section 1 : Imports de module
import math
import numpy as np

# Section 2 : DÃ©finition de fonctions


# Section 3 : Tests de fonctions dÃ©finies et manipulations en mode "script"
v = np.zeros(4)
print(v)

I_4 = np.identity(4)
print(I_4)

M = np.arange(12).reshape(3,4)
print(M)

M_T = np.transpose(M)
print(M_T)

# matrice de taille 10*10 avec des 1 tout autour et des 0 au centre
N = np.ones((10,10))
N[1:-1,1:-1] = 0
print(N)

# aleatoire de taille 10*10 selon loi normale centrée réduite puis normalisée entre 0 et 1
P = np.random.randn(10,10)
P = (P - np.min(P)) / (np.max(P) - np.min(P))
print(P)

# produit matriciel
Q = np.dot(M, I_4)
print(Q)
# Q = M @ I_4
# print(Q)
# ou Q = M.dot(I_4)

print(M @ I_4 + v)

print(M.sum(1))

x = np.array([0.1, 0.2, 0.4])
y = np.array([1., 2., 8.])

# cauchy : je transforme les vecteurs x et y en matrices 2D pour faire la division
# x[:, None] transforme x en matrice colonne
# y[None, :] transforme y en matrice ligne
C = 1 / (x[:, None] - y[None, :])
print(C)

Z = np.random.randn(10,3)
print(Z)
moy = Z.mean(1)
print(moy)

Z_centered = Z - moy[:, None]
print(Z_centered)

print(Z_centered.mean(1))
print(moy[:, None])

# exo de synthèse
notes = np.array(
    [[10, 12],
    [15, 16],
    [18, 12]]
)

# moyenne des etudiant
moyenne = notes.mean(0)
print(moyenne)

# nombre de notes au dessus de 12
nb_sup_12 = (notes > 12).sum()
# nb_sup_12 = (notes >= 12).sum()
print(nb_sup_12)