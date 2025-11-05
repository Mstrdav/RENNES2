import numpy as np

def acp(X, qq, dd):
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
    C_tilde = D @ C  # on comprend pas trop mais ça affiche quelque chose au bout
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
    X = np.array([[2.5, 2.4],
                  [0.5, 0.7],
                  [2.2, 2.9],
                  [1.9, 2.2],
                  [3.1, 3.0],
                  [2.3, 2.7],
                  [2, 1.6],
                  [1, 1.1],
                  [1.5, 1.6],
                  [1.1, 0.9]])

    # Poids des colonnes (qq) et des lignes (dd)
    qq = np.array([1, 1])
    dd = np.array([1/10] * 10)

    result = acp(X, qq, dd)

    print(result)

    # plot !!
    import matplotlib.pyplot as plt
    
    # plot des individus
    plt.scatter(result['C_tilde'][:,0], result['C_tilde'][:, 1], c='blue', label='Individus') # merci l'IA
    for i in range(result['C_tilde'].shape[0]):
        plt.text(result['C_tilde'][i, 0], result['C_tilde'][i, 1], f'I{i+1}', color='blue')

    # affichage
    plt.title('ACP - Projection des individus')
    plt.xlabel('Axe 1')
    plt.ylabel('Axe 2')
    plt.axhline(0, color='grey', lw=1)
    plt.axvline(0, color='grey', lw=1)
    plt.grid()
    plt.legend()
    plt.show()
