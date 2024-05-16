from elasticsearch import Elasticsearch
import json

# Spécifiez les paramètres de connexion.
host = "127.0.0.1"
port = 9200
user = "elastic"
password = "changeme"
my_index ="satisfactionclients_fr"

# Créez un objet client Elasticsearch avec l'authentification.
#es = Elasticsearch(hosts="http://@127.0.0.1:9200")
es = Elasticsearch(['http://127.0.0.1:9200'], basic_auth=(user, password))
# Vérifiez la connexion.
if es.ping():
    # Comptage du nombre de documents dans l'index "my-index"
    count = es.count(index=my_index)

    # Afficher le nombre de documents
    print("Nombre de documents dans l'index 'my-index':", count["count"])
    # Créez une requête pour rechercher tous les documents
    query = {
        "query": {
            "match_all": {}
        }
    }

    # Effectuez la recherche
    results = es.search(index=my_index, body=query)

    # Itérez sur les résultats et affichez les documents
    for hit in results["hits"]["hits"]:
        print(hit["_source"])

    query = {
            "query": {
                    "match": {
                        "Commentaire": {
                            "query": "mauvais"
                        }
                    }
            }
    }
    # Effectuez la recherche
    results = es.search(index=my_index, body=query)

    # Itérez sur les résultats et affichez les documents
    for hit in results["hits"]["hits"]:
        company_name = hit['_source']['Société']
        company_note = hit['_source']['Rating']
        company_avis = hit['_source']['Commentaire']
        company_sentiment= hit['_source']['Sentiment']
        company_motspositifs= hit['_source']['MotsPositifs']
        company_motsnegatifs= hit['_source']['MotsNegatifs']
        print(f"Company: {company_name}, Rating: {company_note}, Avis: {company_avis}, Sentiment:{company_sentiment},Mots positifs:{company_motspositifs}, "
              f"Mots négatifs:{company_motsnegatifs}")


else:
    print("Connexion échouée.")