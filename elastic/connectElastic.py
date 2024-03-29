from elasticsearch import Elasticsearch


# Définir l'URL de la base Elasticsearch
url = "http://localhost:9200"

# Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "changeme"
index_name = "satisfactionclients"

#


# Créer une instance Elasticsearch avec le nom d'utilisateur et le mot de passe
try:
    

    es = Elasticsearch(
            url,
            basic_auth=(username, password),
        )


    # # Vérifier la connexion en obtenant des informations sur le cluster
    info = es.info()
    print(f"Information Elasticsearch:\n{info}")
    
    # Obtenir les informations générales de l'index
    index_info = es.indices.get(index=index_name)
    print(f"Information d'index satisfactionclients: \n{index_info}")
    
    
    # # Afficher le nombre de shards et de répliques
    # print(f"Nombre de shards : {index_info['settings']['index']['number_of_shards']}")
    # print(f"Nombre de répliques : {index_info['settings']['index']['number_of_replicas']}")



    # # # Obtenir la liste de tous les index
    # all_indices = es.indices.get_alias(index="*")

    # # # Afficher l'existence de chaque index
    # for index_name in all_indices:
    #     print(f"L'index '{index_name}' existe.")
    
    
    #     # Obtenir les informations générales de l'index
    #     index_info = es.indices.get(index=index_name)

    #     # Afficher le nombre de shards et de répliques
    #     print(f"Nombre de shards : {index_info['settings']['index']['number_of_shards']}")
    #     print(f"Nombre de répliques : {index_info['settings']['index']['number_of_replicas']}")

    # # Obtenir les mappings de l'index
    # mappings = es.indices.get_mapping(index="satisfactionclients")

    # # Parcourir les types de documents et afficher les champs
    # for doc_type in mappings:
    #     print(f"Type de document : {doc_type}")
    #     for field in mappings[doc_type]['properties']:
    #         print(f"  - {field}")
                
    
except Exception as e:
    print(f"Erreur : {e}")
