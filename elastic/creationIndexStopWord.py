# Creation Index avec les stopwords french, english, dutch pour autres langues non determinees
from elasticsearch import Elasticsearch


#
# # Définir l'URL de la base Elasticsearch
url = "http://localhost:9200"
#
# # Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "changeme"
index_name = "satisfactionclients_other"
index_settings = {
    "number_of_shards": 1,
    "number_of_replicas": 1,
}


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



# Mapping final avec langue, Mots positifs, Mot Négatifs, Sentiments
    mapping = {
        "mappings": {
            "properties": {
                "Domaine": {"type": "text", "analyzer": "standard"},
                "Société": {"type": "text", "analyzer": "standard"},
                "Pays": {"type": "text", "analyzer": "standard"},
                "Personne": {"type": "text"},
                "Commentaire": {"type": "text", "fielddata": True, "analyzer": "standard"},
                "Rating": {"type": "float"},
                "Date": {"type": "date"},
                "Reponse": {"type": "text", "fielddata": True, "analyzer": "standard"},
                "Langue": {"type": "text", "fielddata": True, "analyzer": "language"},
                "MotsPositifs": {"type": "text", "fielddata": True, "analyzer": "standard"},
                "MotsNegatifs": {"type": "text", "fielddata": True, "analyzer": "standard"},
                "Sentiment": {"type": "text", "fielddata": True, "analyzer": "standard"},
            }
        },
        "settings": {
            "analysis": {
                "filter": {
                    "french_stop": {"type": "stop", "stopwords": "_french_"},
                    "english_stop": {"type": "stop", "stopwords": "_english_"},
                    "dutch_stop": {"type": "stop", "stopwords": "_dutch_"}
                },
                "analyzer": {
                    "language": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["french_stop", "english_stop", "dutch_stop"]
                    }
                }
            }
        }
    }

    # Création de l'index avec le mapping spécifié
    success = es.indices.create(index=index_name, body=mapping)


    if success:
        print(f"L'index '{index_name}' a été créé avec succès)")
        index_info = es.indices.get(index=index_name)

        # Affichage des caractéristiques de l'index
        print("Caractéristiques de l'index '{}':".format(index_name))
        print("-----------------------------------------")
        print(index_info[index_name])

except Exception as e:
    print(f"Erreur : {e}")