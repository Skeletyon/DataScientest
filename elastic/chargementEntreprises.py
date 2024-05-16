### Chargement les 3 fichiers json dans les 3 index qui correspondent à la langue détectée
from elasticsearch import Elasticsearch
import json
import datetime
import re
import datetime as dt

#from LibSatisfaction import calculate_average_rating

# On pourait en faire une petite fonction pour etre propres
cheminFichierScrapping = "../scrapping/results/"
current_date = dt.date.today()
f = current_date.strftime('%Y-%m-%d')
jsonFile = cheminFichierScrapping + f + "_entreprises.json"
#jsonFile = cheminFichierScrapping +  "2024-05-11_entreprises.json"

# Définir l'URL de la base Elasticsearch
url = "http://localhost:30003"

# Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "changeme"
# index_name = "satisfactionclients"
index_name_ent = "satisfactionclients_entreprises"

# # Define the mapping
# mapping = {
#     "mappings": {
#         "properties": {
#             "Domaine": {"type": "text", "analyzer": "standard"},
#             "Entreprise": {"type": "text", "analyzer": "standard"},
#             "Note": {"type": "text", "analyzer": "standard"},
#             "Entreprise verifiee": {"type": "text"},
#             "Nombre avis": {"type": "text", "fielddata": True, "analyzer": "standard"},
#         }
#     },
#     "settings": {
#         "analysis": {
#             "filter": {
#                 "french_stop": {"type": "stop", "stopwords": "_french_"}
#             },
#         }
#     }
# }

# Créer une instance Elasticsearch avec le nom d'utilisateur et le mot de passe
try:

    es = Elasticsearch(
        url,
        basic_auth=(username, password),
    )

    # # Vérifier la connexion en obtenant des informations sur le cluster
    info = es.info()
    print(f"Information Elasticsearch:\n{info}")

    print("File:", jsonFile)


    with open(jsonFile, "r") as f:
        data = json.load(f)

    # Envoyer les documents par lot pour optimiser les performances
    for doc in data:
#       doc["Note"]=calculate_average_rating(doc)
        doc["Nombre avis"]=doc["Nombre avis"].replace(",", ".")
        print(doc)
        # Indexation
        es.index(index=index_name_ent, body=doc)

    # Contrôler le nombre de documents charger
    # Verify document count using the correct method
    count = es.search(index=index_name_ent, body={"size": 0})["hits"]["total"]["value"]
    print(f"\nNombre de documents chargés en : {count}")



    print("Chargement complet des données terminé")

except Exception as e:
    print(f"Erreur : {e}")