from elasticsearch import Elasticsearch
import json
import datetime

# Définir l'URL de la base Elasticsearch
url = "http://localhost:9200"

# Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "changeme"
index_name = "satisfactionclients_stopword"
jsonFile = "satisfactionWonderbox.json"

#


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

        es.index(index=index_name, body=doc)
    
    
    # Contrôler le nombre de documents charger
     # Verify document count using the correct method
    count = es.search(index=index_name, body={"size": 0})["hits"]["total"]["value"]
    print(f"\nNombre de documents chargés : {count}")
    print(f"\nNombre de documents : {count}")
    
except Exception as e:
    print(f"Erreur : {e}")
