from elasticsearch import Elasticsearch


url = "http://localhost:9200"

# Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "changeme"


def check_all_indices_exist():
    """
    Vérifie l'existence de tous les index Elasticsearch.

    Args:
        host (str): Adresse IP ou nom d'hôte de votre cluster Elasticsearch.
        port (int): Port Elasticsearch.

    Returns:
        None
    """
    # Se connecter à Elasticsearch
    es = Elasticsearch(
        url,
        basic_auth=(username, password),
    )


    try:
        # Obtenir la liste de tous les index
        all_indices = es.indices.get_alias("*")

        # Afficher l'existence de chaque index
        for index_name in all_indices:
            print(f"L'index '{index_name}' existe.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


# Exemple d'utilisation
check_all_indices_exist()