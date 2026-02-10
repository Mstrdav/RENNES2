# Section 1 : Imports de module
import datetime

# Section 2 : Définition de fonctions
def compte_mots(chaine): return len(chaine.split())
def est_un_fichier_texte(nomFichier): return nomFichier.split(".")[-1] in ["txt", "json", "csv"] and len(nomFichier) >= 5
def table_multiplication(base, multiStart=1, multiEnd=10):
    for i in range(multiStart, multiEnd + 1):
        print(f"{base}*{i}={base*i}")

MASSE_GRAIN = 0.035 # en grammes
PROD_ANNUELLE = 650000000 * 1000 * 1000 # en grammes
NOMBRE_CASES = 64

def masse_total_grains():
    # return sum(MASSE_GRAIN * 2**i for i in range(NOMBRE_CASES))
    return MASSE_GRAIN * (2**(NOMBRE_CASES)-1) # plus efficace

"""
Renvoie  la masse totale de grain divisée par la production annuelle du pays
"""
def annees_prod():
    return masse_total_grains() / PROD_ANNUELLE

"""
Renvoie un triplet (jour, mois, année) correspondant à la date du lendemain

Arguments:
jour  - le jour
mois  - le mois
annee - l'année

Return:
(jour, mois, annee)
"""
def lendemain(jour, mois, annee):
    date = datetime.date(annee, mois, jour)
    # le lendemain
    demain = date + datetime.timedelta(days=1)
    return demain.day, demain.month, demain.year

"""
Affiche la table de multiplication usuelle, au format (pour la base 7)
    7*1=7
    7*2=14
    ...
    7*10=70

Arguments:
base  - la table que l'on veut afficher
"""
def table_multiplication_usuelle(base): table_multiplication(base)

"""
Compte le nombre de lettres majuscules l dans la chaîne s

Arguments:
s - la chaîne de caractères
l - la lettre à compter
"""
def count_upper_letter(s,l): return s.count(l.upper())

# Section 3 : Tests de fonctions définies et manipulations en mode "script
print("------------ Tests de fonctions définies -----------")
print(compte_mots("Bonjour tout le monde"))
print(est_un_fichier_texte("document.txt")) 
print(est_un_fichier_texte("image.png"))

table_multiplication(5, 4, 7)


# print(masse_total_grains())
print(annees_prod())

print(lendemain(15, 3, 2023)) # jour normal
print(lendemain(30, 4, 2023)) # fin de mois
print(lendemain(28, 2, 2020)) # année bissextile
print(lendemain(31, 12, 2023)) # fin d'année

table_multiplication_usuelle(7)

print(count_upper_letter("Bonjour tout le Monde", "o"))
print(count_upper_letter("Bonjour tout le Monde", "M"))

