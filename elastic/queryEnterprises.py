from elasticsearch import Elasticsearch
url = "http://localhost:9200"

# Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "changeme"
# Se connecter à Elasticsearch
es = Elasticsearch(
    url,
    basic_auth=(username, password),
)

index_name="satisfactionclients_entreprises"
# Define the query body
query = {
    "query": {
        "match_all": {}  # Match all documents
    },
    "_source": ["Entreprise", "Note","Nombre avis"],  # Specify fields to return
    "sort": [{"Note": {"order": "desc"}}]  # Sort by 'Note' descending
}

# Execute the search and get the response
response = es.search(index=index_name, body=query)  # Replace 'your_index_name' with your actual index name

# Process and display the results
for hit in response['hits']['hits']:
    company_name = hit['_source']['Entreprise']
    company_note = hit['_source']['Note']
    company_avis = hit['_source']['Nombre avis']
    print(f"Company: {company_name}, Rating: {company_note}, Avis: {company_avis}")