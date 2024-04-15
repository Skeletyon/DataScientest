from elasticsearch import Elasticsearch
import json
import datetime
import re
from LibSatisfaction import mots_pos_neg, detect_language,detect_format_date

# Définir l'URL de la base Elasticsearch
url = "http://localhost:9200"

# Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "changeme"
index_name = "satisfactionclients"

jsonFiles=[ ("WonderboxBelgique.json","Belgique"),
            ("WonderboxFrance.json","France"),
            ("WonderboxHollande.json", "Hollande"),
]

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
    for jsonFile, Pays in jsonFiles:
        print("File:",jsonFile)
        with open(jsonFile , "r") as f:
            data = json.load(f)

        # Envoyer les documents par lot pour optimiser les performances
        for doc in data:
            doc["Domaine"] = "Boutique de cadeaux"
            doc["Société"] = "WonderBox"
            doc["Pays"] = Pays
            # Convert the date to the desired format (yyyy-MM-dd)
            #doc["Date"]  = "Date de l'expérience: 03 avril 2024"

            # Utiliser une expression régulière pour extraire la partie après le ":"
            nouvelle_date = re.sub(r'^.*?:', '', doc["Date"] ).strip()
            nouvelle_date = nouvelle_date.replace(",", "")
            nouvelle_date=nouvelle_date.lower()
            nouvelle_date,format_date = detect_format_date(nouvelle_date)

            if (format_date != "None" ):
                doc["Date"] = datetime.datetime.strptime(nouvelle_date,format_date).strftime("%Y-%m-%d")
            else:
                doc["Date"] =  nouvelle_date

            # detection de la langue du commentaire
            commentaires_non_nuls = list(filter(lambda x: x is not None, doc["Commentaire"]))
            lang = detect_language(commentaires_non_nuls)
            doc["Langue"]=lang

            # Recupérer les mots positifs et negatifs de la phrase
            comment = commentaires_non_nuls[0]
            mots_positifs, mots_negatifs = mots_pos_neg(comment, lang)
            doc["MotsPositifs"]=mots_positifs
            doc["MotsNegatifs"] = mots_negatifs

            # Estimer le sentiment
            if (len(mots_positifs) >0  and len(mots_negatifs) >0 ):
                doc["Sentiment"]   = "neutre"
            elif (len(mots_positifs) > 0 and  float(doc["Rating"]) > 2.5):
                doc["Sentiment"] = "positif"
            elif (len(mots_negatifs) > 0 ):
                doc["Sentiment"] = "negatif"
            else:
                doc["Sentiment"] = "neutre"

            # Indexation
            es.index(index=index_name, body=doc)


        # Contrôler le nombre de documents charger
         # Verify document count using the correct method
        count = es.search(index=index_name, body={"size": 0})["hits"]["total"]["value"]
        print(f"\nNombre de documents chargés : {count}")
        print(f"\nNombre de documents : {count}")

except Exception as e:
    print(f"Erreur : {e}")
