from elasticsearch import Elasticsearch


#
# # Définir l'URL de la base Elasticsearch
url = "http://localhost:9200"
#
# # Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "changeme"


def create_index(es, index_name, index_settings):
  """
  Fonction pour créer un index dans Elasticsearch.

  Args:
      es: Instance de la classe Elasticsearch.
      index_name: Nom de l'index à créer.
      index_settings: Dictionnaire contenant les paramètres de l'index.

  Returns:
      True si l'index a été créé avec succès, False sinon.
  """

  try:
    es.indices.create(index=index_name, body=index_settings)
  except Exception as e:
    print(f"Échec de la création de l'index '{index_name}' : {e}")
    return False

  return True

try:

    es = Elasticsearch(
            url,
            basic_auth=(username, password),
        )



    index_name = "satisfactionclients"
    index_settings = {
        "number_of_shards": 1,
        "number_of_replicas": 1,
    }

    index_sentiment = "sentiments"
        
# Mapping final avec langue, Mots positifs, Mot Négatifs, Sentiments
    mapping = {
        "mappings": {
            "properties": {
                "Domaine": {"type": "text"},
                "Société": {"type": "text"},
                "Pays": {"type": "text"},
                "Personne": {"type": "text"},
                "Commentaire": {"type": "text" , "fielddata": True},
                "Rating" : {"type": "float"},
                "Date": {"type": "date"},
                "Reponse": {"type": "text", "fielddata": True},
                "Langue": {"type": "text", "fielddata": True},
                "MotsPositifs": {"type": "text", "fielddata": True},
                "MotsNegatifsifs": {"type": "text", "fielddata": True},
                "Sentiment": {"type": "text", "fielddata": True},
            }
        }
    }

    mapping_sentiment = {
        "mappings": {
            "properties": {
                "Text": {"type": "text","fielddata": True},
                "Label": {"type": "text" ,"fielddata": True},
            }
        }
    }



    # Création de l'index avec le mapping spécifié
    success = es.indices.create(index=index_name, body=mapping)


    if success:
        print(f"L'index '{index_name}' a été créé avec succès)")
        index_info = es.indices.get(index=index_name)

        # Affichage des caractéristiques de l'index
        print("Caractéristiques de l'index '{}':".format(index_sentiment))
        print("-----------------------------------------")
        print(index_info[index_name])

except Exception as e:
    print(f"Erreur : {e}")