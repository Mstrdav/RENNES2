import pandas as pds
import datetime 
# Création de la fonction permettant d'importer les jeux de données
def load_data(file_path):
    return pds.read_csv(file_path)

# création des tables
table_client = load_data("table_client.csv")
table_commande_reprise = load_data("table_commande_reprise.csv")
table_financement = load_data("table_financement.csv")
table_navigation = load_data("table_navigation_web.csv")
table_nearest_agency = load_data("table_nearest_agency.csv")
table_vehicule = load_data("table_vehicule.csv")

# Exemple de manipulation
table_exemple = pds.merge(table_client,table_commande_reprise,left_on='ID_LEAD',right_on = 'LEAD_ID')
table_exemple['DATE_PANIER'] = pds.to_datetime(table_exemple['DATE_PANIER'])
table_exemple['age'] = table_exemple['DATE_PANIER'].dt.year - table_exemple['YEAR_NAISSANCE']

print(table_exemple.groupby('TYPE_PANIER')['age'].mean())

print(table_exemple.groupby('TYPE_PANIER')['ID_LEAD'].count())


