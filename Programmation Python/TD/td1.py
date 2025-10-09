# Section 1 : Imports de modules
import random
import math
import datetime

# Section 2 : Définition de fonctions
def est_palindrome(mot):
    for i in range (0,len(mot)//2) :
        if mot[i] != mot[len(mot)-1-i] :
            return False
        
    return True

def longueur_mois(mois,an):
    if mois > 12 or mois < 1 :
        return 0
    if mois in [1,3,5,7,8,10,12]: # mois de 31 jours
        return 31
    if mois == 2: # février
        # check bissextile
        if an % 4 == 0:
            return 29
        else:
            return 28
        
    else: return 30 # mois de 30 jours
    

def multiple_mot(nom=str,num=int):
    print(nom*num)

def valeur_hasard():
    return random.random()

def sinus(angle) :
    return math.sin(angle)

def age(jour,mois,annee):
    date_naissance = datetime.date(annee, mois, jour)
    date_maintenant = datetime.date.today()
    return((date_maintenant - date_naissance).days // 365)


# # Section 3 : Tests de fonctions définies et manipulations en mode "script"

# print(sinus(90))
# print(sinus(3.14))
# print(sinus(math.pi))

print(age(9,2,1998))
print(age(23,11,2002))

# multiple_mot("kayak",5)

# replique_1_2 = "Je ne vous jette pas la pierre, Pierre,"
# replique_2_2 = "mais j'étais à deux doigts de m'agacer"
# concat = replique_1_2 + replique_2_2
# print(concat)
# print(len(concat))
# concat_lower = concat.lower()
# print(concat_lower)
# concat_lower_replaced = concat_lower.replace("agacer", "énerver")
# print(concat_lower_replaced)
# print(concat_lower_replaced.count("pierre"))

# print("est_palindrome(\"kayak\")")
# print(est_palindrome("kayak"))
# print("est_palindrome(\"palindrome\")")
# print(est_palindrome("palindrome"))
# print("est_palindrome(\"elle\")")
# print(est_palindrome("elle"))

# print(longueur_mois(9,2025))
# print(longueur_mois(1,2025))
# print(longueur_mois(26,2025))
# print(longueur_mois(2,2025))
# print(longueur_mois(2,2024))

# print('3' * 10) # ok: "333333333"
# print(3 * 10) # ok: 30
# '3' * 10.0 # err: can't multiply seq by non-int (float)
# print('3' + '3') # ok: "33"
# print(3 + 3) # ok: 6
# '3' + 3 # err: can only concat str to str 
