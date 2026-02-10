# Imports
import requests
from graphh import GraphHopper
from pprint import pprint
import credentials

STAR_API_URL = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-bus-vehicules-position-tr/records"


# comment faire pour avoir tous les bus ? cycler les appels a l'API car limit max = 100 alors qu'on a 543 bus sur le réseau
# ou limit = -1 -> on veut tout

def fetch_all_buses():
    buses = []
    limit = 100
    offset = 0

    while True:
        params = {
            'limit': limit,
            'offset': offset,
            'refine': 'etat:En ligne'
        }
        response = requests.get(STAR_API_URL, params=params)
        # print(f"URL construite : {response.url}")
        data = response.json()

        records = data.get('results', [])
        if not records:
            break

        for bus in records:
            buses.append({
                "numerobus": bus["numerobus"],
                "nomcourtligne": bus["nomcourtligne"],
                "destination": bus["destination"],
                "ecartsecondes": bus["ecartsecondes"],
                "position": bus["coordonnees"],
            })
        offset += limit

    return buses

def nb_bus_en_avance(buses):
    count = sum(1 for bus in buses if bus["ecartsecondes"] > 0)
    return count

def liste_ecart_par_ligne(buses):
    lignes = {}
    for bus in buses:
        lignes[bus["nomcourtligne"]] = lignes.get(bus["nomcourtligne"], []) + [bus["ecartsecondes"]]
    return lignes

def retard_moyen_par_ligne(buses):
    lignes = liste_ecart_par_ligne(buses)
    for key in lignes.keys():
        lignes[key] = sum(lignes[key])/len(lignes[key])

    return lignes

# graph hopper

def main():
    buses = fetch_all_buses()
    print(f"Total number of buses fetched: {len(buses)}")

    print(nb_bus_en_avance(buses))
    pprint(retard_moyen_par_ligne(buses))

if __name__ == "__main__":
    main()
