# 22503282 Colin Geindre

# Imports
from abc import ABC, abstractmethod

# Classes et fonctions
class Expression(ABC):
    """
    evaluation de la fonction au point x
    """
    @abstractmethod
    def forward(self, x):
        pass

    """
    gradient de la fonction au point x
    """
    @abstractmethod
    def grad(self, x):
        pass

    """
    fonction de représentation d'une expression
    """
    @abstractmethod
    def __repr__(self):
        pass

    def __add__(self, exp2):
        if isinstance(exp2, (int, float)):
            exp2 = Constante(exp2)
        return Somme(self, exp2)

    def __mul__(self, exp2):
        if isinstance(exp2, (int, float)):
            exp2 = Constante(exp2)
        return Produit(self, exp2)

    def __sub__(self, exp2):
        return Somme(self, Produit(Constante(-1), exp2))

    def __pow__(self, exposant):
        if exposant == 2:
            return Produit(self, self)
        else:
            raise NotImplementedError("Seul l'exposant 2 est implémenté.")

class Constante(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.value}'

    def forward(self, x):
        return self.value

    def grad(self, x):
        return 0

class Variable(Expression):
    def __repr__(self):
        return 'x'

    def forward(self, x):
        return x

    def grad(self, x):
        return 1

class Produit(Expression):
    def __init__(self, *args):
        self.facteurs = args

    def __repr__(self):
        return f'{" * ".join([f'{facteur}' for facteur in self.facteurs])}'
    
    def forward(self, x):
        temp = 1
        for facteur in self.facteurs:
            temp *= facteur.forward(x)
        return temp

    # grad(a*b*c) = a'*b*c + a*b'*c + a*b*c'
    def grad(self, x):
        temp = 0
        for i, facteur in enumerate(self.facteurs):
            prod = 1
            for j, autre_facteur in enumerate(self.facteurs):
                if i == j:
                    prod *= autre_facteur.grad(x)
                else:
                    prod *= autre_facteur.forward(x)

            temp += prod
        return temp

class Somme(Expression):
    def __init__(self, *args):
        self.termes = args

    def __repr__(self):
        return f'({" + ".join([f'{terme}' for terme in self.termes])})'

    def forward(self, x):
        return sum([terme.forward(x) for terme in self.termes])

    def grad(self, x):
        return sum([terme.grad(x) for terme in self.termes])

def descente_de_gradient(expr, x0, p=0.01, iter=1000):
    x = x0
    for _ in range(iter):
        x = x - p * expr.grad(x)
    return x

# Corps du programme
if __name__ == "__main__":
    x = Variable()
    expr = x*x + Constante(2) * (x + Constante(-2))
    print(f'f(x) = {expr}')
    print("f(3) =", expr.forward(3))
    print("f'(3) =", expr.grad(3))
    xmin = round(descente_de_gradient(expr, 0), 8)
    print("Minimum en x =", xmin)
    print("f(xmin) =", expr.forward(xmin))
    print("f'(xmin) =", expr.grad(xmin))

    #  test de definition d'une expression de maniere litterale
    expr2 = x**2 + (x - 2)*2
    print(f'\nf(x) = {expr2}')
    # print("f(3) =", expr2.forward(3))
    # ça marche pas (encore ?)
