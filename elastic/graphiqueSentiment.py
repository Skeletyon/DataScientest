from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt



# Définir l'URL de la base Elasticsearch
url = "http://localhost:9200"

# Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "changeme"
index_name = "satisfactionclients"

query = {
    'query': {
        'match_all': {}  # Retrieve all documents
    }
}

try:
    es = Elasticsearch(
        url,
        basic_auth=(username, password),
    )

    results = es.search(index=index_name, body=query)
    sentiment_data = []
    for doc in results['hits']['hits']:
        sentiment_info = {
            'Langue': doc['_source']['Langue'],
            'Pays': doc['_source']['Pays'],
            'MotsPositifs': doc['_source']['MotsPositifs'],
            'MotsNegatifs': doc['_source']['MotsNegatifs'],
            'Sentiment': doc['_source']['Sentiment']
        }
        sentiment_data.append(sentiment_info)



    # Count occurrences of each sentiment category
    sentiment_counts = {}
    for entry in sentiment_data:
        sentiment = entry['Sentiment']
        if sentiment not in sentiment_counts:
            sentiment_counts[sentiment] = 0
        sentiment_counts[sentiment] += 1

    # Create a pie chart
    plt.pie(sentiment_counts.values(), labels=sentiment_counts.keys(), autopct="%1.1f%%")
    plt.title('Sentiment Distribution Pie Chart')
    plt.show()
    plt.savefig('sentiment_distribution_pie_chart.png')
    print('sentiment_distribution_pie_chart.png')
except Exception as e:
    print(f"Erreur : {e}")
