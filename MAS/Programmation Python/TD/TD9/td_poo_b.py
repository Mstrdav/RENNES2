# Imports
from abc import ABC, abstractmethod

# Classes et fonctions
class CompteSimple:
    def __init__(self, solde=0):
        self.solde = solde

    def __repr__(self):
        return f'Le solde du compte est de {self.solde} Euro(s).'

    def enregistrerOperation(self, op):
        self.solde += op["valeur"]

class CompteCourant:
    def __init__(self, solde=0):
        self.solde = solde
        self.operations = []

    def __repr__(self):
        return f'Le solde du compte courant est de {self.solde} Euro(s).'

    def enregistrerOperation(self, op):
        self.operations.append(op)
        self.solde += op["valeur"]

    def afficherReleve(self):
        for op in self.operations:
            print(f'{op["date"]} - {op["type"]} de {op["valeur"]} Euro(s).')

    def afficherReleveCredit(self):
        for op in self.operations:
            if op["type"] == "credit":
                print(f'{op["date"]} - {op["type"]} de {op["valeur"]} Euro(s).')

    def afficherReleveDebit(self):
        for op in self.operations:
            if op["type"] == "debit":
                print(f'{op["date"]} - {op["type"]} de {op["valeur"]} Euro(s).')

class IntervalleAbstrait (ABC):
    def __init__(self, a, b):
        self.a, self.b = min(a, b), max(a, b)

    def __repr__(self):
        return f'IntervalleAbstrait({self.a},{self.b})'

    @abstractmethod
    def __contains__(self, v):
        pass

class IntervalleOuvert (IntervalleAbstrait):
    def __contains__(self, v):
        return self.a < v < self.b

class IntervalleFerme (IntervalleAbstrait):
    def __contains__(self, v):
        return self.a <= v <= self.b

# Tests
if __name__ == "__main__":
    c = CompteSimple(100)
    print(c)
    c.enregistrerOperation({"valeur": 50, "type": "credit", "date": "2024-01-01"})
    print(c)

    cc = CompteCourant(200)
    print(cc)
    cc.enregistrerOperation({"valeur": -30, "type": "debit", "date": "2024-01-02"})
    cc.enregistrerOperation({"valeur": 90, "type": "debit", "date": "2024-01-03"})
    print(cc)

    print("Relevé complet:")
    cc.afficherReleve()

    print("Relevé des crédits:")
    cc.afficherReleveCredit()
    print("Relevé des débits:")
    cc.afficherReleveDebit()

    # test intervalle
    intervalle_ferme = IntervalleFerme(1, 5)
    print(intervalle_ferme)
    print(3 in intervalle_ferme)  # True
    print(1 in intervalle_ferme)  # True
    intervalle_ouvert = IntervalleOuvert(1, 5)
    print(intervalle_ouvert)
    print(3 in intervalle_ouvert)  # True
    print(1 in intervalle_ouvert)  # False
