# 22503282 Colin Geindre

# Imports
from abc import ABC, abstractmethod

# Classes et fonctions
class Expression(ABC):
    # évaluation de la fonction en x
    @abstractmethod
    def forward(self, x):
        pass

    # calcul de la dérivée
    @abstractmethod
    def grad(self, x):
        pass
