# Section 1 : Imports de module
import math

SPEC_CHAR = ["À", "Â", "Æ", "Ç", "É", "È", "Ê", "Ë", "Î", "Ï", "Ô", "Œ", "Ù", "Û",
"Ü", "Ÿ", "à", "â", "æ", "ç", "é", "è", "ê", "ë", "î", "ï", "ô",
"œ", "ù", "û", "ü", "ÿ"]
REP_CHAR = ["A", "A", "AE", "C", "E", "E", "E", "E", "I", "I", "O", "OE", "U", "U", "U", "Y", "a", "a", "ae", "c", "e", "e", "e", "e", "i", "i", "o", "oe", "u", "u", "u", "y"]
dico = dict(zip(SPEC_CHAR, REP_CHAR))

# Section 2 : Définition de fonctions
def normalise(texte):
    return "".join([char if char not in dico else dico[char] for char in texte])

def dico_chaine(chaine):
    mots = chaine.split()
    dico = {}
    for mot in mots:
        if mot in dico:
            dico[mot] += 1
        else:
            dico[mot] = 1
    return dico

def most_frequent(chaine): # using dico_chaine
    dico = dico_chaine(chaine)
    max_mot = ""
    max_count = 0
    for mot, count in dico.items():
        if count > max_count:
            max_count = count
            max_mot = mot
    return max_mot

def total_ventes(dico):
    return sum(dico.values())

def max_ventes(ventes):
    return max(ventes)

# les sets
def liste_triee_sans_doublon(l):
    return sorted(list(set(l)))

def distinct(l): return len(set(l)) # return len(liste_triee_sans_doublon)

def remove_spaces(texte): return texte.replace(" ", "").replace("\t", "").replace("\n", "").replace("'", "").replace(",", "")

def pangram(texte): return distinct(normalise(remove_spaces(texte))) == 26

# Section 3 : Tests de fonctions définies et manipulations en mode "script"
weird_text = "Dès Noël où un zéphyr haï me vêt de glaçons würmiens, je dîne d'exquis rôtis de bœuf au kir à l'aÿ d'âge mûr et cætera!"
print(weird_text)
print(normalise(weird_text))
test_text = "Ceci est un texte avec des mots avec des mots répétés et des mots uniques"
print(dico_chaine(test_text))
print(most_frequent(test_text))

ventes={"Dupont":14, "Hervy":19, "Geoffroy":15, "Layec":21}
print(total_ventes(ventes))
print(max_ventes(ventes))

l = [6,4,8,2,2,7,4,9,11,0]
print(liste_triee_sans_doublon(l))
print(distinct(l))

text = "Portez ce vieux whisky au juge blond qui fume"
print(pangram(text))
print(pangram("Ceci n'est pas un pangramme"))
print(pangram("Cwm fjord bank glyphs vext quiz")) # pangramme en anglais
print(pangram("J'ai vu un punk afghan et deux clowns aux zygomatiques incroyables"))