#
# TD 3: Les listes
#

import math;

def print_sinus():
    for i in range(0,361):
        print(f'sin({i}°) = sin({math.radians(i)} rad) = {math.sin(math.radians(i))}')

def plusieurs_tables(l_bases):
    return [[i * j for j in range(1, 11)] for i in l_bases]

def puissance_bornee(borne_inf, borne_sup, puissance):
    return  [b**puissance for b in range(borne_inf, borne_sup+1)]

def carre_bornee(borne_inf, borne_sup):
    return puissance_bornee(borne_inf, borne_sup, 2)

def l_taille(l_chaines):
    return [len(s) for s in l_chaines]

def liste_triee_sans_doublon(l):
    # return sorted(list(set(l)))
    new_l = []
    for element in sorted(l):
        if element in new_l: continue
        new_l.append(element)

    return new_l

def mot_le_plus_long(chaine):
    mots = chaine.split()
    tailles = [len(mot) for mot in mots]
    return mots[tailles.index(max(tailles))]

def filter_even(liste):
    return filter(lambda x: x%2==0, liste)
    # return [x for x in liste if x%2==0]

# pour aller plus loin
def liste_plus_trois(liste): return [x + 3 for x in liste]
def float_text(liste): return [float(x) for x in liste.split()]

# TESTS
print_sinus()
print(plusieurs_tables([2, 3, 4, 5]))
print(puissance_bornee(3, 7, 2))
print(carre_bornee(3, 7))
print(l_taille([[1,2,3], range(0,6), "Hello, World!"]))
l = [6,4,8,2,2,7,4,9,11,0]
print(liste_triee_sans_doublon(l))
print(mot_le_plus_long("Bonjour Michaela comment allez vous ?"))
print(filter_even(l))

print(liste_plus_trois(l))
print(float_text("1.0 3.14 7 8.4 0.0"))