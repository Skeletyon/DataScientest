from elasticsearch import Elasticsearch
# Définir l'URL de la base Elasticsearch
url = "http://localhost:9200"

# Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "elastic"

# Créer le document JSON de l'utilisateur
utilisateur = {
  "username": "client_kibana",
  "password": "client_kibana",
  "roles": ["InterfaceKiabana"],
  "metadata": {
    "email": "mon_utilisateur@example.com",
    "full_name": "Kibana Utilisateur"
  }
}



# Créer une instance Elasticsearch avec le nom d'utilisateur et le mot de passe
try:

    
    es = Elasticsearch(
        url,
        http_auth=(username, password),
    )

    # Vérifier la connexion en obtenant des informations sur le cluster
    info = es.info()
    print(info)
  
    # Envoyer la requête API pour créer l'utilisateur
    es.security.put_user(username="client_kibana", body=utilisateur)

    # Vérifier la création de l'utilisateur
    utilisateur_existe = es.security.get_user(username="client_kibana")

    if utilisateur_existe:
        print("L'utilisateur a été créé avec succès")
    else:
     print("Une erreur est survenue lors de la création de l'utilisateur")

  
except Exception as e:
    print(f"Erreur : {e}")