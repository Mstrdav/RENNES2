# 22503282 Colin Geindre

# 1. Imports et variables globales
import requests

AMIS_API_URL = "https://my-json-server.typicode.com/rtavenar/fake_api/adresses_amis"
HOTELS_API_URL = "https://tabular-api.data.gouv.fr/api/resources/3ce290bf-07ec-4d63-b12b-d0496193a535/data/"

# 2. Fonctions
# On peut filter les hôtels par code postal en ajoutant un paramètre "CODE POSTAL__exact" à l'URL de la requête.
def get_code_postaux():
    response = requests.get(AMIS_API_URL)
    amis_data = response.json()
    code_postaux = {ami['adresse']['code_postal'] for ami in amis_data}
    return code_postaux

def get_hotels_by_code_postaux(code_postaux):
    for code_postal in code_postaux:
        print(f"\nHôtels dans le code postal {code_postal} :")
        url = HOTELS_API_URL
        params = {"CODE POSTAL__exact": code_postal}
        while True:
            response = requests.get(url, params=params)
            hotels_data = response.json()
            next = hotels_data['links']['next'] # s'il y a plus que 20 résultats, l'API renvoie un lien vers la page suivante
            # print(next) # c'était pour vérifier

            for hotel in hotels_data['data']:
                print(f"* {hotel.get('NOM COMMERCIAL')}, {hotel.get('ADRESSE')},  {hotel.get('CODE POSTAL')} {hotel.get('COMMUNE')}")
            if next:
                url = next
            else:
                break
        
# 3. Programme principal
if __name__ == "__main__":
    code_postaux = get_code_postaux()
    get_hotels_by_code_postaux(code_postaux)

    # Un test avec Toulouse (31000) pour voir si la pagination fonctionne
    print(f"\nTest avec le code postal 31000\n------------------------------")
    get_hotels_by_code_postaux(['31000'])