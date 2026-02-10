import numpy as np
import csv

def acp(X, qq, dd, scale=True):
    """
    ACP
    """
    n, p = X.shape

    # petites vérifications, ça mange pas de pain
    if qq.shape[0] != p:
        raise ValueError(f"Le vecteur qq doit avoir {p} éléments")
    if dd.shape[0] != n:
        raise ValueError(f"Le vecteur dd doit avoir {n} éléments")
    if not np.all(qq > 0):
        raise ValueError("Les poids des colonnes (qq) doivent être > 0") # pourquoi ? je sais plus

    if scale:
        # centrage et réduction
        means = np.mean(X, axis=0)
        stds = np.std(X, axis=0, ddof=1)  # écart-type échantillon
        X = (X - means) / stds
    
    # (a) Créer les matrices Q et D
    D = np.diag(dd)
    Q = np.diag(qq)

    # (b) Calculer VQ puis ses vecteurs propres et valeurs propres.
    V = X.T @ D @ X

    # Calcul de M = Q^(1/2) * V * Q^(1/2)
    qq_sqrt = np.sqrt(qq)
    Q_sqrt = np.diag(qq_sqrt)
    Q_inv_sqrt = np.diag(1.0 / qq_sqrt)
    
    M = Q_sqrt @ V @ Q_sqrt

    # Diagonalisation de M (symétrique) par 'eigen'
    # On prend eigh plutot que eig parce que M est symétrique
    eigenvalues, B = np.linalg.eigh(M)

    # Comme R et Python calcule les mêmes vecteurs mais au signe près, on force le signe pour avoir la même chose que R
    for k in range(p):
        if B[0, k] < 0:
            B[:, k] = -B[:, k]

    # Tri par ordre décroissant (eigh trie par ordre croissant)
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    B = B[:, idx]

    # Calcul de A = Q^(-1/2) * B
    A = Q_inv_sqrt @ B
    
    # (c) Calculer les vecteurs propres D-normés à l'unité de WD, à l'aide des formules de transition
    # formules de transition : C_k = 1/sqrt(lambda_k) * X * A_k
    lambdas = eigenvalues
    C = np.zeros((n, p))
    for k in range(p):
        C[:, k] = (1 / np.sqrt(lambdas[k])) * (X @ A[:, k])

    # (d) Calculer les pourcentages d'inertie des axes A
    intertie_totale = np.sum(lambdas)
    pourcentages = (lambdas / intertie_totale)

    # (e) Calculer les coordonnées des lignes C_tilde et des colonnes A_tilde
    C_tilde = D @ C  # si on ne scale pas par D, l'échelle est différente, mais toujours pas celle de R
    A_tilde = Q @ A 

    # on renvoie tout
    return {
        'inerties_partielles': pourcentages,
        'A': A,
        'C': C,
        'A_tilde': A_tilde,
        'C_tilde': C_tilde
    }

# tests !!!
if __name__ == "__main__":
    # Matrice de données X (exemple de données piquées d'internet)
    # read from alcool.csv
    alcool = csv.reader(open("alcool.csv"), delimiter=',')
    header = next(alcool)  # skip header
    data = []
    for row in alcool:
        # data can be either a country, or float values
        data.append([float(x) for x in row[1:]])  # skip country name
    X = np.array(data)

    # Poids des colonnes (qq) et des lignes (dd)
    qq = np.array([1/len(X[0])] * len(X[0]))
    dd = np.array([1/len(X)] * len(X))

    result = acp(X, qq, dd)

    # plot !!
    import matplotlib.pyplot as plt

    # plot des inerties partielles
    plt.bar(range(1, len(result['inerties_partielles']) + 1), result['inerties_partielles'] * 100)
    plt.title("Pourcentages d'inertie des axes")
    plt.xlabel("Axe")
    plt.ylabel("Pourcentage d'inertie (%)")
    plt.xticks(range(1, len(result['inerties_partielles']) + 1))
    plt.grid()
    plt.show()
    
    # plot des individus
    plt.scatter(result['C_tilde'][:,0], result['C_tilde'][:, 1], c='blue', label='Individus')
    for i in range(result['C_tilde'].shape[0]):
        plt.text(result['C_tilde'][i, 0], result['C_tilde'][i, 1], f'I{i+1}', color='blue')

    # affichage
    plt.title('ACP - Projection des individus')
    plt.xlabel(f'Dim 1 ({round(result['inerties_partielles'][0]*100, 2)}%)')
    plt.ylabel(f'Dim 2 ({round(result['inerties_partielles'][1]*100, 2)}%)')
    plt.axhline(0, color='grey', lw=1)
    plt.axvline(0, color='grey', lw=1)
    plt.grid()
    plt.legend()
    plt.show()

    # plot des variables, avec cercle unité et flèches
    # plt.scatter(result['A_tilde'][:,0], result['A_tilde'][:, 1], c='red', label='Variables')
    for i in range(result['A_tilde'].shape[0]):
        plt.text(result['A_tilde'][i, 0], result['A_tilde'][i, 1], header[i+1], color='red')  # +1 to skip country name
    
    circle = plt.Circle((0, 0), 0.36, color='grey', fill=False, linestyle='--') # todo: calculer la vraie valeur de l'unité, avec ce problème de scaling
    plt.gca().add_artist(circle)
    
    for i in range(result['A_tilde'].shape[0]):
        plt.arrow(0, 0, result['A_tilde'][i, 0], result['A_tilde'][i, 1], color='red', head_width=0.01, head_length=0.02, length_includes_head=True, alpha=0.5)

    # echelle un petit peu plus grande pour voir les flèches
    plt.xlim(-0.4, 0.4)
    plt.ylim(-0.4, 0.4)

    plt.title('ACP - Projection des variables')
    plt.xlabel(f'Dim 1 ({round(result['inerties_partielles'][0]*100, 2)}%)')
    plt.ylabel(f'Dim 2 ({round(result['inerties_partielles'][1]*100, 2)}%)')
    plt.axhline(0, color='grey', lw=1)
    plt.axvline(0, color='grey', lw=1)
    plt.grid()
    plt.legend()
    plt.show()
