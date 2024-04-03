from elasticsearch import Elasticsearch
import json
import datetime
from LibSatisfaction import mots_pos_neg, detect_language

# Définir l'URL de la base Elasticsearch
url = "http://localhost:9200"

# Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "changeme"
index_name = "satisfactionclients"
jsonFile = "satisfactionWonderbox.json"

#
# # Mapping final avec langue, Mots positifs, Mot Négatifs, Sentiments
#     mapping = {
#         "mappings": {
#             "properties": {
#                 "Personne": {"type": "text"},
#                 "Commentaire": {"type": "text" , "fielddata": True},
#                 "Rating" : {"type": "float"},
#                 "Date": {"type": "date"},
#                 "Reponse": {"type": "text", "fielddata": True},
#                 "Langue": {"type": "text", "fielddata": True},
#                 "MotsPositifs": {"type": "text", "fielddata": True},
#                 "MotsNegatifsifs": {"type": "text", "fielddata": True},
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
   
    with open(jsonFile , "r") as f:
        data = json.load(f)

    # Envoyer les documents par lot pour optimiser les performances
    for doc in data:
        
        # Convert the date to the desired format (yyyy-MM-dd)
        doc["Date"] = datetime.datetime.strptime(doc["Date"], "%B %d, %Y").strftime("%Y-%m-%d")

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
        elif (len(mots_positifs) > 0):
            doc["Sentiment"] = "positif"
        elif (len(mots_negatifs) > 0):
            doc["Sentiment"] = "negatif"
        else:
            doc["Sentiment"]   = "neutre"

        # Indexation
        es.index(index=index_name, body=doc)


    # Contrôler le nombre de documents charger
     # Verify document count using the correct method
    count = es.search(index=index_name, body={"size": 0})["hits"]["total"]["value"]
    print(f"\nNombre de documents chargés : {count}")
    print(f"\nNombre de documents : {count}")
    
except Exception as e:
    print(f"Erreur : {e}")
