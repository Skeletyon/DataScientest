from elasticsearch import Elasticsearch
import json

# Définir l'URL de la base Elasticsearch
url = "http://localhost:9200"

# Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "elastic"
index_name = "satisfactionclients_fr"
jsonFile = "satisfactionWonderbox.json"

 
# Définition du mapping (schéma) de l'index
mapping = {
    "mappings": {
        "properties": {
            "Personne": {"type": "text"},
            "Commentaire": {"type": "text","fielddata": True},
            "Rating" : {"type": "float"},
            "Date": {"type": "date"},
            "Reponse": {"type": "text","fielddata": True},
        }
    }
}

# Mots positifs/negatifs  en anglais
positive_words = ["happy", "great", "excellent", "satisfied"]
negative_words = ["sad", "bad", "poor", "disappointed"]


# Mots positifs/negatifs  en anglais
positifs_mots= ["bon", "très bon", "excellent", "satisfait"]
negatifs_mots = ["mauvais", "déçu", "pauvre", "instisfait"]




# 
# Créer une instance Elasticsearch avec le nom d'utilisateur et le mot de passe
try:

    
    es = Elasticsearch(
        url,
        basic_auth=(username, password),
    )


# Afficher le nom des personnes qui donnent 1 note > 3


    # Récupérer le mapping de l'index spécifié
    mapping = es.indices.get_mapping(index=index_name)

    # Afficher le mapping par tranche de 10 propriétés à la fois
    properties = mapping[index_name]["mappings"]["properties"]
    count = 0
    for prop_name, prop_info in properties.items():
        print(f"Propriété : {prop_name}")
        print(f"Type : {prop_info['type']}\n")
    
    
    # Définir la requête pour récupérer tous les documents de l'index
    query_all_documents = {
        "query": {
            "match_all": {}  # Correspond à tous les documents
        }
}

    # Exécuter la requête pour récupérer tous les documents de l'index
    result = es.search(index=index_name, body=query_all_documents, size=10)  # Récupérer jusqu'à 10 documents pour commencer
    
    # Convertir le résultat en format JSON
    json_result = json.dumps(result['hits']['hits'], indent=4)
    # Afficher le résultat au format JSON
    print(json_result)
    
    # # Afficher le contenu des documents récupérés
    # for hit in result['hits']['hits']:
    #     print(hit['_source'])  # Afficher le contenu du document
        
        
    # query_rating = {
    #     "query": {"range": {"Rating": {"lt": 2}}},  # Use range for numerical comparison
    #     "sort": [{"Rating": {"order": "desc"}}],
    #     "from": 50,
    #     "size": 50,
    # }

    # results = es.search(index=index_name, body=query_rating)
    # count = results["hits"]["total"]["value"]
    # print(f"\nNombre total de personnes avec une note supérieure à 4 : {count}")

    # # Afficher le nom de la personne pour chaque document
    # for hit in results["hits"]["hits"]:
    #     print(f"Nom : {hit['_source']['Personne']} - Note: {hit['_source']['Rating']}")


#     #################################################
#     query_positive_comments = {
#     "query": {
#         "bool": {
#             "should": [
#                 {"match": {"Commentaire": word}} for word in positive_words
#             ]
#         }
#     }
#     }

#     # Exécuter la requête pour compter les commentaires positifs
#     result = es.count(index=index_name, body=query_positive_comments)

#     # Afficher le nombre de commentaires positifs
#     print("Nombre de commentaires positifs:", result['count'])


#     #################################################
#     query_negative_comments = {
#     "query": {
#         "bool": {
#             "should": [
#                 {"match": {"Commentaire": word}} for word in negative_words
#             ]
#         }
#     }
# }

#     # Exécuter la requête pour compter les commentaires positifs
#     result = es.count(index=index_name, body=query_negative_comments)

#     # Afficher le nombre de commentaires positifs
#     print("Nombre de commentaires negatifs:", result['count'])
  
  
#     query_positive_comments = {
#         "query": {
#          "bool": {
#             "should": [
#                 {"match": {"Commentaire": word}} for word in positive_words
#             ]
#         }
#     },
#         "_source": ["Personne","Rating", "Commentaire"],
#         "size": 1000  # Spécifier les champs à récupérer
#     }

#     # Exécuter la requête pour récupérer les commentaires positifs
#     result = es.search(index=index_name , body=query_positive_comments)  # Taille de la réponse limitée à 1000 commentaires

# # Afficher les Ratings et les commentaires des commentaires positifs
#     for hit in result['hits']['hits']:
#         print("Personne:", hit['_source']['Personne'])
#         print("Rating:", hit['_source']['Rating'])
#         print("Commentaire:", hit['_source']['Commentaire'])
   
   
   # Requête de recherche avec agrégation Terms
   # Nom de l'index et du champ que vous souhaitez analyser
    index_name = "satisfactionclients_stopword"
    field_name = "Commentaire"
    search_body = {
        "size": 0,
        "aggs": {
            "unique_words": {
                "terms": {
                    "field": field_name,
                    "size": 10000  # Nombre maximal de termes à récupérer, ajustez si nécessaire
                }
            }
    }
}

    # Exécution de la recherche
    response = es.search(index=index_name, body=search_body)

    # Récupération des termes uniques
    unique_words = response["aggregations"]["unique_words"]["buckets"]

    # Affichage des termes uniques
    
# Affichage des termes et de leur comptage
    for bucket in unique_words:
        term = bucket["key"]
        count = bucket["doc_count"]
        print(f"Terme : {term}, {count}")

    
except Exception as e:
    print(f"Erreur : {e}")
    