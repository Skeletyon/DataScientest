from elasticsearch import Elasticsearch
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report


# Connexion à Elasticsearch
# Spécifiez les paramètres de connexion.
host = "127.0.0.1"
port = 9200
user = "elastic"
password = "changeme"
index ="satisfactionclients"
index_sentiment = "sentiments"

# Créez un objet client Elasticsearch avec l'authentification.
#es = Elasticsearch(hosts="http://@127.0.0.1:9200")
es = Elasticsearch(['http://127.0.0.1:9200'], basic_auth=(user, password))




# Récupération des commentaires depuis Elasticsearch
results = es.search(index=index, body={"query": {"match_all": {}}})
comments = [hit['_source']['Commentaire'] for hit in results['hits']['hits']]
sentiments = [hit['_source']['Sentiment'] for hit in results['hits']['hits']]

# Division des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(comments, sentiments, test_size=0.2, random_state=42)

# Concaténer chaque liste de mots pour former une seule chaîne de caractères
X_train_concatenated = [' '.join(comment) for comment in X_train]

# Prétraitement des données : Vectorisation TF-IDF
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train_concatenated)
X_test_tfidf = vectorizer.transform(X_test)
# Entraînement d'un modèle de classification SVM linéaire
model = LinearSVC()
model.fit(X_train_tfidf, y_train)

# Prédiction sur l'ensemble de test
predictions = model.predict(X_test_tfidf)

# Évaluation du modèle
print(classification_report(y_test, predictions))
# Index des données dans Elasticsearch


