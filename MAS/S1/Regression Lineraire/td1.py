# import numpy as np

# # graines de pois de senteur de Galton
# data = np.array([
#     [21, 17.5],
#     [20, 17.3],
#     [19, 16],
#     [18, 16.3],
#     [17, 15.6],
#     [16, 16],
#     [15, 15.3]
# ])

# X = data[:, 0]
# Y = data[:, 1]
# n = len(X)

# # moyenne
# mx = np.mean(X)
# my = np.mean(Y)

# # variance
# vx = np.var(X, ddof=0)  # population variance

# # covariance
# cxy = np.cov(X, Y, ddof=0)[0][1]  # population covariance

# # coefficients de la regression
# a = cxy / vx
# b = my - a * mx

# print(f"y = {a:.4f} * x + {b:.4f}")

# SANS NUMPY
# graines de pois de senteur de Galton
data = [
    [21, 17.5],
    [20, 17.3],
    [19, 16],
    [18, 16.3],
    [17, 15.6],
    [16, 16],
    [15, 15.3]
]
n = len(data)
X = [data[i][0] for i in range(n)]
Y = [data[i][1] for i in range(n)]
mx = sum(X) / n
my = sum(Y) / n
print(f"mx = {mx}, my = {my}")

vx = sum((X[i] - mx) ** 2 for i in range(n)) / n
print(f"vx = {vx}")

cxy = sum((X[i] - mx) * (Y[i] - my) for i in range(n)) / n
print(f"cxy = {cxy}")

a = cxy / vx
b = my - a * mx
print(f"y = {a:.4f} * x + {b:.4f}")

# résidus
residus = [Y[i] - (a * X[i] + b) for i in range(n)]
print("résidus =", residus)

# somme des carrés des résidus
sse = sum(r ** 2 for r in residus)
print(f"sse = {sse}")

# moyenne des résidus
m_residus = sum(residus) / n
print(f"moyenne des résidus = {m_residus}")

# variance des résidus
var_residus = sse / n
print(f"variance des résidus = {var_residus}")