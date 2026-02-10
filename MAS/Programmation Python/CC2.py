# 22503282

# imports
import requests
import numpy as np

# fonctions et classes

"""
ModeleAffine(W, b)
- W numpy array de dimension (d,) des poids du modèle
- b scalaire de l'ordonnée à l'origine
"""
class ModeleAffine():
    def __init__(self, W, b):
        self.W = W
        self.b = b

    def __repr__(self):
        return f'Modèle affine ayant pour poids {self.W} et pour ordonnée à l\'origine {self.b}'

    def predict(self, X):
        return X @ self.W + self.b

"""
ModeleLineaire(W) - inherit ModeleAffine
- W numpy array de dimension (d,) des poids du modèle
- L'ordonnée à l'origine est nulle
"""
class ModeleLineaire(ModeleAffine):
    def __init__(self, W):
        super().__init__(W, 0)

    def __repr__(self):
        return f'Modèle linéaire ayant pour poids {self.W}'

# --------------- API ----------------
""" 
isPosBounded(pos, bounds) - TRUE si pos est dans bounds
- pos : coordonnées au format [lat, long]
- bounds : objet de coordonées limites au format 
    {
        "min_lat": min_lat,
        "max_lat": max_lat,
        "min_lon": min_lon,
        "max_lon": max_lon
    }
"""
def isPosBounded(pos, bounds):
    return pos[0] >= bounds["min_lat"] and pos[0] <= bounds["max_lat"] and pos[1] >= bounds["min_lon"] and pos[1] <= bounds["max_lon"]

"""
listGPX() - return la liste des fichiers (leurs noms) sur l'api
"""
def listGPX():
    return requests.get("https://trails-api.onrender.com/files").json()["files"]

"""
pprintGPX(gpx, pos) - affiche joliment un trace et la position, avec la distance totale et le dénivelé
- gpx : objet au format 
    {
        "file": nom_du_fichier,
        "total_distance_km": distance_totale_en_kilometres,
        "total_ascent_m": denivele_en_metres,
        "bounds": objet_bounds_cf_isPosBounded
    }
"""
def pprintGPX(gpx, pos):
    print(f'{pos} - {gpx["file"]} :\n\tlongueur de la trace : {gpx["total_distance_km"]} km\n\ttotal denivelé : {gpx["total_ascent_m"]} m')

"""
printAllBoundingGpx(pos) - affiche via pprintGPX tous les fichiers dont la zone couvre la position
- pos : position au format [lat, lon]
"""
def printAllBoundingGpx(pos):
    for file in listGPX():
        file_data = requests.get("https://trails-api.onrender.com/files/" + file).json()
        if file_data.get("detail", 0):
            continue # ce fichier n'a pas été trouvé sur l'API
        if isPosBounded(pos, file_data["bounds"]):
            pprintGPX(file_data, pos)

# tests
if __name__ == "__main__":
    print("------- Exercice POO --------\n")
    poids1 = np.array([1,5,4])
    poids2 = np.array([4,0])
    modele1 = ModeleAffine(poids1, 2.5)
    modele2 = ModeleLineaire(poids2)

    print(modele1)
    print(modele2)
    print("prediction modele 1 en X = [0,0,4]")
    print(modele1.predict(np.array([0,0,4])))
    print(f"prediction modele 1 en X =\n{np.ones((4,2))}")
    print(modele2.predict(np.ones((4,2))))

    
    print("\n\n------- Exercice API --------\n")
    bounds1 = {
        "min_lat": 57.1,
        "max_lat": 59.7,
        "min_lon": 32.5,
        "max_lon": 39.0,
    }
    print(f"La position [58, 34] est-elle (oui) dans {bounds1}")
    print(isPosBounded([58,34], bounds1))
    print(f"La position [57, 34] est-elle (non) dans {bounds1}")
    print(isPosBounded([57,34], bounds1))
    print("Liste des GPX")
    print(listGPX())
    pos1 = [45.5, 4.43]
    print(f"Test final, tous les GPX qui englobent la position {pos1}")
    printAllBoundingGpx(pos1)

