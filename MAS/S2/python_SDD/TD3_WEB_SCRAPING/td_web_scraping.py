import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup, Tag, NavigableString
import pickle
from multiprocessing import Pool, cpu_count

# Définition des fonctions
##########################

def extract_text(soup):
    texte = ""
    # boucle sur les enfants de soup
    for c in soup.children:
        # si l'enfant est un NavigableString : on récupère le texte
        # dans c.string, et on retire les espaces en trop (.strip())
        if type(c) == NavigableString:
            if (c.string).strip() != "":
                texte += " "+(c.string).strip()
        # si l'enfant est un tag qui n'est pas un bouton (balise button)
        # on va chercher le texte à l'intérieur et on le rajoute au texte déjà récupéré
        elif type(c) == Tag and c.name != "button" :  
            texte += extract_text(c)

    return texte


# Programme principal
#####################
if __name__ == '__main__':
    # écrire tout votre code dans ce bloc (nécessaire pour la programmation parallèle)
    pass  # instruction nulle à supprimer 