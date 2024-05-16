from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from elasticsearch import Elasticsearch
from datetime import datetime
import subprocess
import os

app = FastAPI()

# Spécifiez les paramètres de connexion Elasticsearch
host = "elasticsearch:9200"
port = 9200
user = "elastic"
password = "changeme"

# Créez un objet client Elasticsearch avec l'authentification de base
es = Elasticsearch([f'http://{host}'], basic_auth=(user, password))

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


@app.get("/top-companies-stats")
async def get_top_companies_stats(index: str = "satisfactionclients_entreprises"):
    # Définir la requête Elasticsearch pour récupérer les données des meilleures entreprises
    query = {
        "size": 5,
        "sort": [
            {"Nombre avis": {"order": "desc"}},  # Trier par nombre d'avis décroissant
            {"Note": {"order": "desc"}}  # Trier par note décroissante
        ],
        "_source": ["Entreprise", "Note", "Nombre avis"]
    }

    try:
        # Exécuter la requête Elasticsearch
        response = es.search(index=index, body=query)

        # Extraire les données des entreprises
        top_companies_stats = [{
            "Entreprise": hit['_source']['Entreprise'],
            "Note": hit['_source']['Note'],
            "Nombre_avis": hit['_source']['Nombre avis']
        } for hit in response['hits']['hits']]

        return top_companies_stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")



@app.get("/bottom-companies-stats")
async def get_bottom_companies_stats(index: str = "satisfactionclients_entreprises"):
    # Définir la requête Elasticsearch pour récupérer les données des moins bonnes entreprises
    query = {
        "size": 5,
        "sort": [
            {"Nombre avis": {"order": "asc"}},  # Trier par nombre d'avis croissant
            {"Note": {"order": "asc"}}  # Trier par note croissante
        ],
        "_source": ["Entreprise", "Note", "Nombre avis"]
    }

    try:
        # Exécuter la requête Elasticsearch
        response = es.search(index=index, body=query)

        # Extraire les données des entreprises
        bottom_companies_stats = [{
            "Entreprise": hit['_source']['Entreprise'],
            "Note": hit['_source']['Note'],
            "Nombre_avis": hit['_source']['Nombre avis']
        } for hit in response['hits']['hits']]

        return bottom_companies_stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Elasticsearch: {str(e)}")




@app.get("/run-machine-learning")
async def run_machine_learning():
    try:
        # Récupérer le chemin absolu du répertoire contenant main.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construire le chemin absolu vers machinelearning.py
        script_path = os.path.join(current_dir, "../elastic/machinelearning.py")
        
        # Exécuter le script machinelearning.py en tant que processus séparé avec l'interpréteur Python
        result = subprocess.run(["python3", script_path], capture_output=True, text=True)

        # Vérifier si l'exécution s'est terminée avec succès
        if result.returncode == 0:
            # Renvoyer la sortie du script comme réponse à l'API
            return {"output": result.stdout}
        else:
            # Si une erreur s'est produite, renvoyer le message d'erreur
            return {"error": result.stderr}
    except Exception as e:
        # Si une exception est levée, renvoyer l'erreur
        return {"error": str(e)}
