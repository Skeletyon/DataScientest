from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from elasticsearch import Elasticsearch
from datetime import datetime

app = FastAPI()

# Spécifiez les paramètres de connexion Elasticsearch
host = "127.0.0.1"
port = 9200
user = "elastic"
password = "changeme"

# Créez un objet client Elasticsearch avec l'authentification de base
es = Elasticsearch([f'http://{host}:{port}'], basic_auth=(user, password))

@app.get("/comments")
async def get_comments(index: str = "satisfactionclients_fr"):
    # Définir la requête Elasticsearch pour récupérer tous les commentaires
    query = {
        "query": {
            "match_all": {}
        }
    }
    
    # Exécuter la requête Elasticsearch
    try:
        response = es.search(index=index, body=query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")
    
    # Extraire les commentaires de la réponse
    comments = [hit["_source"]["Commentaire"] for hit in response["hits"]["hits"]]
    
    return {"comments": comments}


@app.get("/positive-comments")
async def get_positive_comments(index: str = "satisfactionclients_fr", date_min: Optional[str] = Query(None), date_max: Optional[str] = Query(None)):
    # Définir la requête Elasticsearch pour récupérer les commentaires positifs
    positive_query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"Sentiment": "positif"}}
                ]
            }
        }
    }

    # Ajouter des filtres de date si des valeurs sont fournies
    if date_min or date_max:
        range_filter = {}
        if date_min:
            range_filter["gte"] = date_min
        if date_max:
            range_filter["lte"] = date_max
        positive_query["query"]["bool"]["filter"] = [{"range": {"Date": range_filter}}]

    try:
        # Exécuter la requête Elasticsearch
        response = es.search(index=index, body=positive_query)
        # Extraire les commentaires de la réponse
        comments = [hit["_source"]["Commentaire"] for hit in response["hits"]["hits"]]
        return {"positive_comments": comments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")


@app.get("/positive-comments/stats")
async def get_positive_comments_stats(index: str = "satisfactionclients_fr", date_min: Optional[str] = Query(None), date_max: Optional[str] = Query(None)):
    # Définir la requête Elasticsearch pour récupérer les statistiques des commentaires positifs
    positive_query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"Sentiment": "positif"}}
                ]
            }
        }
    }

    # Ajouter des filtres de date si des valeurs sont fournies
    if date_min or date_max:
        range_filter = {}
        if date_min:
            range_filter["gte"] = date_min
        if date_max:
            range_filter["lte"] = date_max
        positive_query["query"]["bool"]["filter"] = [{"range": {"Date": range_filter}}]

    try:
        # Exécuter la requête Elasticsearch pour compter les commentaires positifs
        positive_comments_response = es.count(index=index, body=positive_query)
        positive_comments_count = positive_comments_response["count"]

        # Exécuter la requête Elasticsearch pour compter le nombre total de commentaires
        total_comments_response = es.count(index=index)
        total_comments_count = total_comments_response["count"]

        return {"positive_comments_count": positive_comments_count, "total_comments_count": total_comments_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")


@app.get("/negative-comments")
async def get_negative_comments(index: str = "satisfactionclients_fr", date_min: Optional[str] = Query(None), date_max: Optional[str] = Query(None)):
    # Définir la requête Elasticsearch pour récupérer les commentaires négatifs
    negative_query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"Sentiment": "negatif"}}
                ]
            }
        }
    }

    # Ajouter des filtres de date si des valeurs sont fournies
    if date_min or date_max:
        range_filter = {}
        if date_min:
            range_filter["gte"] = date_min
        if date_max:
            range_filter["lte"] = date_max
        negative_query["query"]["bool"]["filter"] = [{"range": {"Date": range_filter}}]

    try:
        # Exécuter la requête Elasticsearch
        response = es.search(index=index, body=negative_query)
        # Extraire les commentaires de la réponse
        comments = [hit["_source"]["Commentaire"] for hit in response["hits"]["hits"]]
        return {"negative_comments": comments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")


@app.get("/negative-comments/stats")
async def get_negative_comments_stats(index: str = "satisfactionclients_fr", date_min: Optional[str] = Query(None), date_max: Optional[str] = Query(None)):
    # Définir la requête Elasticsearch pour récupérer les statistiques des commentaires négatifs
    negative_query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"Sentiment": "negatif"}}
                ]
            }
        }
    }

    # Ajouter des filtres de date si des valeurs sont fournies
    if date_min or date_max:
        range_filter = {}
        if date_min:
            range_filter["gte"] = date_min
        if date_max:
            range_filter["lte"] = date_max
        negative_query["query"]["bool"]["filter"] = [{"range": {"Date": range_filter}}]

    try:
        # Exécuter la requête Elasticsearch pour compter les commentaires négatifs
        negative_comments_response = es.count(index=index, body=negative_query)
        negative_comments_count = negative_comments_response["count"]

        # Exécuter la requête Elasticsearch pour compter le nombre total de commentaires
        total_comments_response = es.count(index=index)
        total_comments_count = total_comments_response["count"]

        return {"negative_comments_count": negative_comments_count, "total_comments_count": total_comments_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")


@app.get("/comments-with-response")
async def get_comments_with_response_count(index: str = "satisfactionclients_fr"):
    # Définir la requête Elasticsearch pour compter les commentaires avec une réponse de l'entreprise
    response_query = {
        "query": {
            "exists": {"field": "Reponse"}
        }
    }
    
    try:
        # Exécuter la requête Elasticsearch pour compter les commentaires avec une réponse non vide
        response_comments_response = es.count(index=index, body=response_query)
        response_comments_count = response_comments_response["count"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")
    
    return {"comments_with_response_count": response_comments_count}

