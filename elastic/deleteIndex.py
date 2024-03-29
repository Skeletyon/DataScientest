from elasticsearch import Elasticsearch
import json
import datetime

# Définir l'URL de la base Elasticsearch
url = "http://localhost:9200"

# Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "elastic"
index_name = "satisfactionclients_stopword"
jsonFile = "satisfactionWonderbox.json"


es = Elasticsearch(
        url,
        basic_auth=(username, password),
    )


# Vérifier si l'index existe avant de le supprimer
if es.indices.exists(index=index_name):
    # Supprimer l'index
    es.indices.delete(index=index_name)
    print(f"L'index '{index_name}' a été supprimé avec succès.")
else:
    print(f"L'index '{index_name}' n'existe pas.")