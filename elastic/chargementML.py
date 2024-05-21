### Chargement les 3 fichiers json dans les 3 index qui correspondent à la langue détectée
from elasticsearch import Elasticsearch
import json
import datetime
import re
from LibSatisfaction import mots_pos_neg, detect_language, detect_format_date, detect_sentiment_fr, \
    detect_sentiment_other
import datetime as dt

# On pourait en faire une petite fonction pour etre propres
cheminFichierScrapping = "../scrapping/results/"
current_date = dt.date.today()
f = current_date.strftime('%Y-%m-%d')
# f="2024-05-13"
belgique = cheminFichierScrapping + "WonderboxBelgique_" + f + ".json"
france = cheminFichierScrapping + "WonderboxFrance_" + f + ".json"
hollande = cheminFichierScrapping + "WonderboxHollande_" + f + ".json"

# Définir l'URL de la base Elasticsearch
url = "http://localhost:30003"

# Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "changeme"

# index_name = "satisfactionclients"
index_name = "satisfactionclients_ml"
jsonFile = "../scrapping/results/colorlandFrance_2024-05-16.json"
# jsonFiles=[
#              ("WonderboxFrance.json","France")
#  ]
#
# # Mapping final avec langue, Mots positifs, Mot Négatifs, Sentiments
#     mapping = {
#         "mappings": {
#             "properties": {
#                 "Domaine": {"type": "text"},
#                 "Société": {"type": "text"},
#                 "Pays":{"type": "text"},
#                 "Personne": {"type": "text"},
#                 "Commentaire": {"type": "text" , "fielddata": True},
#                 "Rating" : {"type": "float"},
#                 "Date": {"type": "date"},
#                 "Reponse": {"type": "text", "fielddata": True},
#                 "Langue": {"type": "text", "fielddata": True},
#                 "MotsPositifs": {"type": "text", "fielddata": True},
#                 "MotsNegatifs": {"type": "text", "fielddata": True},
#                 "Sentiment": {"type": "text", "fielddata": True},
#             }
#         }
#     }
# #


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
    print("Pays:", "France")

    with open(jsonFile, "r") as f:
        data = json.load(f)

    # Envoyer les documents par lot pour optimiser les performances
    for doc in data:
        # detection de la langue du commentaire
        doc["Domaine"] = "Boutique de cadeaux"
        doc["Société"] = "WonderBox"
        doc["Pays"] = "France"
        # Convert the date to the desired format (yyyy-MM-dd)
        # doc["Date"]  = "Date de l'expérience: 03 avril 2024"

        # Utiliser une expression régulière pour extraire la partie après le ":"
        nouvelle_date = re.sub(r'^.*?:', '', doc["Date"]).strip()
        nouvelle_date = nouvelle_date.replace(",", "")
        nouvelle_date = nouvelle_date.lower()
        nouvelle_date, format_date = detect_format_date(nouvelle_date)

        if (format_date != "None"):
            doc["Date"] = datetime.datetime.strptime(nouvelle_date, format_date).strftime("%Y-%m-%d")
        else:
            doc["Date"] = nouvelle_date

        es.index(index=index_name, body=doc)

    # Contrôler le nombre de documents charger
    # Verify document count using the correct method
    count = es.search(index=index_name, body={"size": 0})["hits"]["total"]["value"]
    print(f"\nNombre de documents chargés en : {count}")

    print("Chargement complet des données terminé")

except Exception as e:
    print(f"Erreur : {e}")
