# 22503282 Colin Geindre
# IA utilisée pour générer de jolis tests : https://gemini.google.com/share/47963d2c3227

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

    def __truediv__(self, exp2):
        if isinstance(exp2, (int, float)):
            exp2 = Constante(exp2)
        return Division(self, exp2)

    def __sub__(self, exp2):
        return Somme(self, Produit(Constante(-1), exp2))

    def __pow__(self, exposant):
        if exposant == 2:
            return Produit(self, self)
        else:
            raise NotImplementedError("Seul l'exposant 2 est implémenté.") # TODO: implémenter d'autres exposants

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
        self.facteurs = [Constante(arg) if isinstance(arg, (int, float)) else arg for arg in args]

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

class Division(Expression):
    def __init__(self, numerateur, denominateur):
        self.numerateur = Constante(numerateur) if isinstance(numerateur, (float, int)) else numerateur
        self.denominateur = Constante(denominateur) if isinstance(denominateur, (float, int)) else denominateur

    def __repr__(self):
        return f'{self.numerateur} / {self.denominateur}'

    def forward(self, x):
        return self.numerateur.forward(x) / self.denominateur.forward(x)

    def grad(self, x):
        temp = self.denominateur.forward(x) # pour éviter un double appel
        return (self.numerateur.grad(x) * temp - self.numerateur.forward(x) * self.denominateur.grad(x)) / (temp ** 2)

class Somme(Expression):
    def __init__(self, *args):
        self.termes = [Constante(arg) if isinstance(arg, (int, float)) else arg for arg in args]

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

# ==========================================
# ZONE DE TESTS - Genération initiale par Gemini: https://gemini.google.com/share/47963d2c3227
# ==========================================
if __name__ == "__main__":
    # Fonction utilitaire pour afficher joliment les résultats
    def check(nom, valeur, attendu):
        # On tolère une petite marge d'erreur pour les floats
        succes = abs(valeur - attendu) < 1e-6
        icone = "✅" if succes else "❌"
        print(f"   {icone} {nom:<15} : Trouvé {valeur:<10.4f} | Attendu {attendu}")

    print("\n=== DÉBUT DES TESTS ===\n")

    # 1. Test simple : f(x) = x
    x = Variable()
    print(f"--- Test 1: Fonction Identité f(x) = {x} ---")
    check("Forward (x=3)", x.forward(3), 3)
    check("Grad (x=3)", x.grad(3), 1)

    # 2. Test opérations arithmétiques : f(x) = 3x + 5
    f1 = x * 3 + 5
    print(f"\n--- Test 2: Affine f(x) = {f1} ---")
    # f(2) = 3*2 + 5 = 11
    # f'(2) = 3
    check("Forward (x=2)", f1.forward(2), 11)
    check("Grad (x=2)", f1.grad(2), 3)

    # 3. Test puissance et soustraction : f(x) = x^2 - 4x + 1
    f2 = (x ** 2) - (x * 4) + 1
    print(f"\n--- Test 3: Polynôme f(x) = {f2} ---")
    # Pour x = 3 : 
    # Forward: 3^2 - 4*3 + 1 = 9 - 12 + 1 = -2
    # Grad: 2x - 4 => 2*3 - 4 = 2
    check("Forward (x=3)", f2.forward(3), -2)
    check("Grad (x=3)", f2.grad(3), 2)

    # 4. Test division : f(x) = (2x + 3) / (x - 1)
    f3 = (x * 2 + 3) / (x - 1)
    print(f"\n--- Test 4: Division f(x) = {f3} ---")
    # Pour x = 3 :
    check("Forward (x=3)", f3.forward(3), 4.5)
    check("Grad (x=3)", f3.grad(3), -1.25)

    # 5. Test Descente de Gradient
    # Minimiser f(x) = x^2 (le minimum est à 0)
    print(f"\n--- Test 4: Descente de gradient sur f(x) = x^2 ---")
    parabole = x ** 2
    point_depart = 10.0
    learning_rate = 0.1
    iterations = 100
    
    min_trouve = descente_de_gradient(parabole, point_depart, learning_rate, iterations)
    
    print(f"   Départ à x={point_depart}")
    print(f"   Minimum théorique : 0.0")
    check("Résultat", min_trouve, 0.0)

    # Minimiser f(x) = (x-2)^2 (le minimum est à 2)
    # Note : (x-2)^2 = x^2 - 4x + 4
    print(f"\n--- Test 5: Descente de gradient sur f(x) = (x-2)^2 ---")
    f4 = (x - 2)**2
    min_trouve_2 = descente_de_gradient(f4, x0=0.0, p=0.01, iter=2000)
    
    print(f"   Fonction : {f4}")
    print(f"   Minimum théorique : 2.0")
    check("Résultat", min_trouve_2, 2.0)

    print("\n=== FIN DES TESTS ===")
