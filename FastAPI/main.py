from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch

app = FastAPI()

# Spécifiez les paramètres de connexion Elasticsearch
host = "127.0.0.1"
port = 9200
user = "elastic"
password = "changeme"
my_index ="satisfactionclients_en"

# Créez un objet client Elasticsearch avec l'authentification de base
es = Elasticsearch(['http://127.0.0.1:9200'], basic_auth=(user, password))

@app.get("/comments")
async def get_comments():
    # Définir la requête Elasticsearch pour récupérer tous les commentaires
    query = {
        "query": {
            "match_all": {}
        }
    }
    
    # Exécuter la requête Elasticsearch
    try:
        response = es.search(index=my_index, body=query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")
    
    # Extraire les commentaires de la réponse
    comments = [hit["_source"]["Commentaire"] for hit in response["hits"]["hits"]]
    
    return {"comments": comments}


@app.get("/positive-comments")
async def get_positive_comments_count():
    # Définir la requête Elasticsearch pour compter les commentaires avec un sentiment positif
    positive_query = {
        "query": {
            "match": {
                "Sentiment": "positif"
            }
        }
    }
    
    # Exécuter la requête Elasticsearch pour compter les commentaires positifs
    try:
        positive_comments_response = es.count(index=my_index, body=positive_query)
        positive_comments_count = positive_comments_response["count"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")
    
    # Exécuter la requête Elasticsearch pour compter le nombre total de commentaires
    try:
        total_comments_response = es.count(index=my_index)
        total_comments = total_comments_response["count"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")
    
    return {"total_comments": total_comments, "positive_comments_count": positive_comments_count}



@app.get("/negative-comments")
async def get_negative_comments_count():
    # Définir la requête Elasticsearch pour compter les commentaires avec un sentiment négatif
    negative_query = {
        "query": {
            "match": {
                "Sentiment": "negatif"
            }
        }
    }
    
    # Exécuter la requête Elasticsearch pour compter les commentaires négatifs
    try:
        negative_comments_response = es.count(index=my_index, body=negative_query)
        negative_comments_count = negative_comments_response["count"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")
    
    # Exécuter la requête Elasticsearch pour compter le nombre total de commentaires
    try:
        total_comments_response = es.count(index=my_index)
        total_comments = total_comments_response["count"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")
    
    return {"total_comments": total_comments, "negative_comments_count": negative_comments_count}

@app.get("/comments-with-response")
async def get_comments_with_response_count():
    # Définir la requête Elasticsearch pour compter les commentaires avec une réponse de l'entreprise
    response_query = {
        "query": {
            "bool": {
                "must_not": {
                    "term": {"Reponse.keyword": "None"}
                }
            }
        }
    }
    
    # Exécuter la requête Elasticsearch pour compter les commentaires avec une réponse
    try:
        response_comments_response = es.count(index=my_index, body=response_query)
        response_comments_count = response_comments_response["count"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")
    
    return {"comments_with_response_count": response_comments_count}

@app.get("/comments-above-rating/{min_rating}")
async def get_comments_above_rating_count(min_rating: float):
    # Définir la requête Elasticsearch pour compter les commentaires avec une note supérieure à la valeur minimale spécifiée
    rating_query = {
        "query": {
            "range": {
                "Rating": {
                    "gt": min_rating
                }
            }
        }
    }
    
    # Exécuter la requête Elasticsearch pour compter les commentaires avec une note supérieure à la valeur minimale spécifiée
    try:
        rating_comments_response = es.count(index=my_index, body=rating_query)
        rating_comments_count = rating_comments_response["count"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")
    
    # Exécuter la requête Elasticsearch pour compter le nombre total de commentaires
    try:
        total_comments_response = es.count(index=my_index)
        total_comments = total_comments_response["count"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")
    
    return {"total_comments": total_comments, "comments_above_rating_count": rating_comments_count}