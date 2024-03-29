from elasticsearch import Elasticsearch
#import  ssl
# trust="/home/nguyenhn/logiciel/elk/elasticsearch-8.13.0/config/certs/transport.p12"
# keystore="/home/nguyenhn/logiciel/elk/elasticsearch-8.13.0/config/certs"
# ctx = ssl.create_default_context()
# ctx.verify_mode = ssl.CERT_REQUIRED
# ctx.check_hostname = True
#
# es_host = "localhost"
# es_port = 9200
# es_username = "elastic"
# es_password = "changeme"

# # Load truststore content (assuming PEM format)
# with open(keystore, "rb") as f:
#   ctx.load_cert_chain(f)  # Load server certificate and any CA certificates


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

    # Create connection with SSL context
    # es = Elasticsearch(
    #     hosts=[{"host": es_host, "port": es_port}],
    #     http_auth=(es_username, es_password),
    #     use_ssl=True,
    #     ssl_context=ctx
    # )
    es = Elasticsearch(
            url,
            basic_auth=(username, password),
        )


    index_name = "satisfactionclients_stopword"
    index_settings = {
        "number_of_shards": 1,
        "number_of_replicas": 1,
    }
    
        
    # Définition du mapping (schéma) de l'index
    # mapping = {
    #     "mappings": {
    #         "properties": {
    #             "Personne": {"type": "text"},
    #             "Commentaire": {"type": "text"},
    #             "Rating" : {"type": "float"},
    #             "Date": {"type": "date"},
    #             "Reponse": {"type": "text"},
    #         }
    #     }
    # }

# Définition du mapping (schéma) de l'index avec un analyzer français
    mapping = {
        "mappings": {
            "properties": {
                "Personne": {"type": "text"},
                "Commentaire": {"type": "text" , "analyzer": "french","fielddata": True},
                "Rating" : {"type": "float"},
                "Date": {"type": "date"},
                "Reponse": {"type": "text", "analyzer": "french","fielddata": True},
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