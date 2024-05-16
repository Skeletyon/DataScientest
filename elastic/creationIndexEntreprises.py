### Création l'index avec French stopwords

from elasticsearch import Elasticsearch

#
# # Définir l'URL de la base Elasticsearch
url = "http://localhost:30003"
#
# # Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "changeme"
index_name = "satisfactionclients_entreprises"
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


    # Define the mapping
    mapping = {
        "mappings": {
            "properties": {
                "Domaine": {"type": "text", "fielddata": True, "analyzer": "standard"},
                "Entreprise": {"type": "keyword","index": True},
                "Note": {"type": "float"},
                "Entreprise verifiee": {"type": "text"},
                "Nombre avis": {"type": "float"},
                "5": {"type": "text"},
                "4": {"type": "text"},
                "3": {"type": "text"},
                "2": {"type": "text"},
                "1": {"type": "text"},
            }
        },
        "settings": {
            "analysis": {
                "filter": {
                    "french_stop": {"type": "stop", "stopwords": "_french_"}
                },
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