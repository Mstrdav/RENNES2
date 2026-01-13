################################################################################
# Importation de fonctions externes :
import json
from datetime import datetime, timedelta
import re

# Definition locale de fonctions :
def init_liste_chantiers(data):
    liste_chantiers = []
    for dico in data:
        chantier = Chantier(dico)
        liste_chantiers.append(chantier)
    return liste_chantiers

def list_chantiers_en_cours(liste_chantiers, date = datetime.now()):
    return [chantier for chantier in liste_chantiers if chantier.en_cours(date)]

def planning(liste_chantiers, qid, date = datetime.now().strftime("%d/%m/%y %H:%M:%S")):
    date = datetime.strptime(date, "%d/%m/%y %H:%M:%S")
    temp = f"Planning des chantiers au quartier {Chantier.quartiers[qid]} au {date} :"
    print("-" * len(temp))
    print(temp)
    print("-" * len(temp))
    for quartier in liste_chantiers:
        if qid in quartier.quartiers_id:
            print(f"- {quartier.clean_str_from_date(date)}")

def dump_list_chantiers_json(liste_chantiers, filename):
    with open(filename, 'w') as f:
        json.dump([chantier.json_dictionnary() for chantier in liste_chantiers], f, indent=4, ensure_ascii=False)


################################################################################
# Definition des classes :
class Chantier:
    quartiers = {}
    def __init__(self, dico):
        self.quartiers_id = []
        if dico["quartier"] == None:
            for key, val in re.findall('([0-9]+) - ([^,]+)', dico["commune"]):
                Chantier.quartiers[key] = val
                self.quartiers_id.append(key)
        else:
            for key, val in re.findall('([0-9]+) - ([^,]+)', dico["quartier"]):
                Chantier.quartiers[key] = val
                self.quartiers_id.append(key)
        self.id = dico["id"]
        self.localisation = dico["localisation"]
        self.type = dico["type"]
        self.libelle = ("travaux " + dico["libelle"]) if dico["libelle"] else "travaux"
        self.perturbation = dico["niv_perturbation"]
        # read ISO 8601 date strings and remove timezone info
        self.debut = datetime.fromisoformat(dico["date_deb"]).replace(tzinfo=None)
        self.fin = datetime.fromisoformat(dico["date_fin"]).replace(tzinfo=None)

    def __repr__(self):
        # nom du ou des quartiers, localisation du jour/mois/annee heure:minute:seconde au jour/mois/annee heure:minute:seconde : libellé (type, perturbation)
        quartiers_noms = [Chantier.quartiers[qid] for qid in self.quartiers_id]
        return f"{' + '.join(quartiers_noms)}, {self.localisation} du {self.debut.day}/{self.debut.month}/{self.debut.year} {self.debut.hour}:{self.debut.minute}:{self.debut.second} au {self.fin.day}/{self.fin.month}/{self.fin.year} {self.fin.hour}:{self.fin.minute}:{self.fin.second} : {self.libelle} ({self.type}, {self.perturbation})"

    def clean_str_from_date(self, date):
        temp1 = f"{self.localisation} ({self.type}) : chantier "
        temp2 = f" en cours (fin dans {(date - self.fin).days} jours et {(date - datetime.now()).seconds / 3600} heures)" if self.en_cours(date)else (f"terminé (depuis {(date - self.fin).days} jours et {(date - self.fin).seconds / 3600} heures)" if self.termine(date) else f"à venir (début dans {(self.debut - date).days} jours et {(self.debut - date).seconds / 3600} heures)")
        return temp1 + temp2

    def en_cours(self, date):
        return self.debut <= date <= self.fin

    def termine(self, date):
        return date > self.fin

    def a_venir(self, date):
        return date < self.debut

    def json_dictionnary(self):
        return {
            "id": self.id,
            "quartier": ' + '.join([f"{qid} - {Chantier.quartiers[qid]}" for qid in self.quartiers_id]),
            "localisation": self.localisation,
            "type": self.type,
            "libelle": self.libelle,
            "niv_perturbation": self.perturbation,
            "date_deb": self.debut.isoformat(),
            "date_fin": self.fin.isoformat()
        }

    






################################################################################
# Corps principal du programme :
if __name__ == '__main__':
    # recuperation des travaux
    with open('travaux.json', 'r') as f:
        travaux = json.load(f)
    
    liste_chantiers = init_liste_chantiers(travaux)
    print(liste_chantiers[0])

    # tests des methodes de la classe Chantier
    date_test = datetime(2025, 6, 15)
    print(f"Date de test : {date_test}")
    print(f"En cours : {liste_chantiers[0].en_cours(date_test)}")
    print(f"Termine : {liste_chantiers[0].termine(date_test)}")
    print(f"A venir : {liste_chantiers[0].a_venir(date_test)}")

    # test de la fonction list_chantiers_en_cours
    chantiers_en_cours = list_chantiers_en_cours(liste_chantiers, date_test)
    print(f"Chantiers en cours au {date_test} :")
    for chantier in chantiers_en_cours:
        print(chantier)

    # test de la fonction planning
    qid_test = '8'
    planning(liste_chantiers, qid_test, date_test.strftime("%d/%m/%y %H:%M:%S"))

    # test de la fonction dump_list_chantiers_json
    dump_list_chantiers_json(liste_chantiers, 'travaux_dump.json')



    
