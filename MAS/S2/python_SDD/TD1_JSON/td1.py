################################################################################
# Importation de fonctions externes :
import json
from datetime import datetime, timedelta

# Definition locale de fonctions :

def init_liste_chantiers(data):
    # liste_chantiers = []
    # for data_chantier in data:
    #     le_chantier = Chantier(data_chantier)
    #     liste_chantiers.append(le_chantier)
    
    # return liste_chantiers
    return [Chantier(data_chantier) for data_chantier in data]  # la même chose en liste en compréhension

def liste_chantiers_en_cours(liste_chantiers, date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S") # chaine de caractères qui représente
                                                                # la date actuelle 
    # liste_en_cours = []

    # for un_chantier in liste_chantiers:
    #     if un_chantier.en_cours(date_str):
    #         liste_en_cours.append(un_chantier)
    
    # return liste_en_cours

    # la même chose avec une liste en compréhension :
    return [un_chantier for un_chantier in liste_chantiers if un_chantier.en_cours(date_str)]

def affiche_planning_chantiers(liste_chantiers, id_quartier, date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S") # chaine de caractères qui représente
                                                                # la date actuelle
    print(f"Planning des chantiers du quartier {Chantier.quartiers[id_quartier]} au {date_str}:")
    for un_chantier in liste_chantiers:
        if id_quartier in un_chantier.quartier_ids:
            if un_chantier.a_venir(date_str):
                # afficher "début dans X jours et Y heures"
                duree = un_chantier.debut - datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
                jours = duree.days
                heures = duree.seconds//3600
                print(f"{un_chantier.localisation} ({un_chantier.type}) : chantier à venir (début dans {jours} jours et {heures} heures)")
            elif un_chantier.en_cours(date_str):
                # afficher "fin dans X jours et Y heures"
                duree = un_chantier.fin - datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
                jours = duree.days
                heures = duree.seconds//3600
                print(f"{un_chantier.localisation} ({un_chantier.type}) : chantier en cours (fin dans {jours} jours et {heures} heures)")
            elif un_chantier.termine(date_str):
                # afficher "terminé depuis X jours et Y heures"
                duree = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S") - un_chantier.fin
                jours = duree.days
                heures = duree.seconds//3600
                print(f"{un_chantier.localisation} ({un_chantier.type}) : chantier terminé (terminé depuis {jours} jours et {heures} heures)")
                

################################################################################
# Definition des classes :

class Chantier:
    quartiers = {} # attribut de classe qui fera l'association id_quartier->nom_quartier

    def __init__(self, dico_chantier):
        self.id = dico_chantier['id']
        self.localisation  = dico_chantier['localisation']
        self.type = dico_chantier['type']
        self.perturbation = "perturbation inconnue" if dico_chantier['niv_perturbation'] is None else dico_chantier['niv_perturbation']

        # découpage des quartiers (ou communes si pas de quartier)
        if dico_chantier['quartier'] is not None:
            liste_quartiers = dico_chantier['quartier'].split(", ")
        else :
            #print(dico_chantier['id'])
            liste_quartiers = dico_chantier['commune'].split(", ")
        # exemple pour le chantier d'indice 24 :
        # ['12 - Bréquigny','35281 - Saint-Jacques-de-la-Lande']

        # récupération des identifiants des quartiers
        self.quartier_ids = []  # liste vide au départ
        for quartier in  liste_quartiers:
            liste_elements = quartier.split(' - ', maxsplit = 1)
            # exemple pour "9 - Cleunay / Arsenal - Redon / La Courrouze"
            # ['9', 'Cleunay / Arsenal', 'Redon / La Courrouze']
            identifiant = liste_elements[0]
            nom = liste_elements[1]
            self.quartier_ids.append(identifiant)

            # remplissage de l'attribut de classe quartiers (dictionnaire)
            if identifiant not in Chantier.quartiers:
                Chantier.quartiers[identifiant] = nom
        
        # libellé
        self.libelle = "travaux" if dico_chantier['libelle'] is None else "travaux "+dico_chantier['libelle']
        # attributs de date
        self.debut = datetime.fromisoformat(dico_chantier["date_deb"]).replace(tzinfo=None)
        self.fin = datetime.fromisoformat(dico_chantier["date_fin"]).replace(tzinfo=None)


    def __repr__(self):
        noms_quartiers = " + ".join([Chantier.quartiers[ident] for ident in self.quartier_ids])
        chaine = noms_quartiers
        chaine += ", "+self.localisation
        chaine += self.debut.strftime(" du %d/%m/%Y %H:%M:%S")
        chaine += self.fin.strftime(" au %d/%m/%Y %H:%M:%S")
        chaine += " : "+self.libelle
        chaine += " ("+self.type+", "+self.perturbation+")"
        return chaine
    
    def en_cours(self, date_str):
        return  self.debut <= datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S") <= self.fin # type booléen
    
    def termine(self, date_str):
        return  self.fin < datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S") # type booléen

    def a_venir(self, date_str):
        return  datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S") < self.debut # type booléen

    def json_dictionnary(self):
        dico = {}
        dico['id'] = self.id
        dico['quartier'] = " + ".join([Chantier.quartiers[id] for id in self.quartier_ids])
        dico['localisation'] = self.localisation
        dico['libelle'] = self.libelle
        dico['type'] = self.type
        dico['perturbation'] = self.perturbation
        dico['debut'] = self.debut.strftime("%d/%m/%Y %H:%M:%S")
        dico['fin'] = self.fin.strftime("%d/%m/%Y %H:%M:%S")
        return dico

def dump_liste_chantiers_JSON(filename, liste_chantiers):
    with open(filename, 'wt', encoding='utf-8') as o_file:
        json.dump([chantier.json_dictionnary() for chantier in liste_chantiers],
                  o_file,
                  ensure_ascii=False,
                  indent=4)

################################################################################
# Corps principal du programme :
if __name__ == '__main__':
    
    # Question 1.3
    with open("travaux.json", 'rt', encoding='utf8') as json_file:
        data_json = json.load(json_file)
    
    # print(data_json)
    print(data_json[0])

    # Question 2.1
    chantier_test = Chantier(data_json[4])
    print(chantier_test.quartier_ids)
    print(chantier_test.libelle)
    print(Chantier.quartiers)

    # # Question 2.2
    print(chantier_test)

    # # Question 2.3
    liste_chantiers = init_liste_chantiers(data_json)
    print(liste_chantiers)
    print(len(liste_chantiers))

    # # Question 3.1
    print(chantier_test.debut)
    print(chantier_test.fin)

    # # Question 3.2
    # print(chantier_test)

    # # Question 3.3
    print("="*100)
    print("Au 13/01/2026 à 00:00:00 :")
    print(f"En cours : {chantier_test.en_cours('13/01/2026 00:00:00')}")
    print(f"Terminé : {chantier_test.termine('13/01/2026 00:00:00')}")
    print(f"A venir : {chantier_test.a_venir('13/01/2026 00:00:00')}")

    print("Au 01/07/2026 à 00:00:00 :")
    print(f"En cours : {chantier_test.en_cours('01/07/2026 00:00:00')}")
    print(f"Terminé : {chantier_test.termine('01/07/2026 00:00:00')}")
    print(f"A venir : {chantier_test.a_venir('01/07/2026 00:00:00')}")

    print("Au 28/10/2024 à 00:00:00 :")
    print(f"En cours : {chantier_test.en_cours('28/10/2024 00:00:00')}")
    print(f"Terminé : {chantier_test.termine('28/10/2024 00:00:00')}")
    print(f"A venir : {chantier_test.a_venir('28/10/2024 00:00:00')}")


    # # Question 4.1
    print("="*100)
    liste_en_cours = liste_chantiers_en_cours(liste_chantiers, "13/01/2026 00:00:00")
    for un_chantier in liste_en_cours:
        print('-'*50)
        print(un_chantier)

    print("="*100)
    liste_en_cours_now = liste_chantiers_en_cours(liste_chantiers)
    print(f"Nombre de chantiers en cours aujourd'hui : {len(liste_en_cours_now)}")

    # Question 4.2
    print("="*100)
    affiche_planning_chantiers(liste_chantiers, '1')

    # # Question 4.3
    # print("="*100)
    # print(chantier_test.json_dictionnary())

    # # Question 4.4
    # dump_liste_chantiers_JSON("chantiers.json", liste_chantiers)
