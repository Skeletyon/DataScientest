from elasticsearch import Elasticsearch
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.metrics import mean_squared_error
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Définir l'URL de la base Elasticsearch
url = "http://localhost:9200"

# Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "changeme"
#index_name = "satisfactionclients"

index_name_fr = "satisfactionclients_fr"
index_name_en = "satisfactionclients_en"
index_name_other = "satisfactionclients_other"

indexList=[ "satisfactionclients_fr",
            "satisfactionclients_en",
            "satisfactionclients_other"
]

#### A changer #####
my_index=index_name_fr

es = Elasticsearch(
    url,
    basic_auth=(username, password),
)


# Définissez  requête  moyenne rating
requete = {
  "size": 0,
  "aggs": {
    "moyenne_rating": {
      "avg": {
        "field": "Rating"
      }
    }
  }
}
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)
    return scores['compound'], scores['pos'], scores['neg']

def extract_sentiment_features(doc):
    if isinstance(doc['Commentaire'], list):
        text_commentaire = ""
        for item in doc['Commentaire']:
            if item is not None:
                text_commentaire += item + " "
        text_commentaire = text_commentaire.strip()  # Remove trailing space
    else:
        text_commentaire = doc['Commentaire']

    comment_sentiment = analyze_sentiment(text_commentaire)

    if isinstance(doc['Reponse'], list):
        text_reponse = ""
        for item in doc['Reponse']:
            if item is not None:
                text_reponse += item + " "
        text_reponse = text_reponse.strip()  # Remove trailing space
    else:
        text_reponse = doc['Reponse']


    response_sentiment = analyze_sentiment(text_reponse)

    return {
        'Sentiment_Score': comment_sentiment[0] + response_sentiment[0],
        'Positive_Score': comment_sentiment[1] + response_sentiment[1],
        'Negative_Score': comment_sentiment[2] + response_sentiment[2],
    }

for my_index in indexList:

    # Retrieve data from Elasticsearch
    docs = es.search(index=my_index, body={'query': {'match_all': {}}}, size=10000)  # Adjust size as needed
 #   docs = es.search(index=my_index, body={'query': {'match_all': {}}})
    # Extract features and target (rating)
    X = []
    y = []

    for doc in docs['hits']['hits']:
        features = extract_sentiment_features(doc['_source'])
        X.append(list(features.values()))
        y.append(doc['_source']['Rating'])




    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict ratings on test data
    y_pred = model.predict(X_test)

    # Calcul de la moyenne des ratings prédits
    average_predicted_rating = np.mean(y_pred)

    # Evaluate model performance (optional)

    # Convert string data to numeric format
    y_test_numeric = np.array(y_test, dtype=np.float64)
    y_pred_numeric = np.array(y_pred, dtype=np.float64)

    # Now calculate mean squared error
    mse = mean_squared_error(y_test_numeric, y_pred_numeric)

    print(f"Database : {my_index}" )
    print(f"Mean Squared Error: {mse:.2f}")  # Evaluate model fit
    print("Moyenne des ratings prédits sur les données de test:", average_predicted_rating)



    # Exécutez la requête de recherche
    resultat = es.search(index=my_index, body=requete)
    # Récupérez la moyenne des ratings
    moyenne_rating = resultat["aggregations"]["moyenne_rating"]["value"]
    print("Moyenne des ratings en base:", moyenne_rating)


# Prediction
my_index_ml = "satisfactionclients_ml"
docs = es.search(index=my_index_ml, body={'query': {'match_all': {}}}, size=10000)  # Adjust size as needed
#   docs = es.search(index=my_index, body={'query': {'match_all': {}}})
# Extract features and target (rating)
X = []
y = []

for doc in docs['hits']['hits']:
    features = extract_sentiment_features(doc['_source'])
    X.append(list(features.values()))
    y.append(doc['_source']['Rating'])


# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# Predict ratings on test data
y_pred = model.predict(X_test)

# Calcul de la moyenne des ratings prédits
average_predicted_rating = np.mean(y_pred)

print(f"Prédiction sur la base   : {my_index_ml}" )
print("Moyenne des ratings prédits sur les nouvelles données:", average_predicted_rating)

# Exécutez la requête de recherche
resultat = es.search(index=my_index_ml, body=requete)
# Récupérez la moyenne des ratings
moyenne_rating = resultat["aggregations"]["moyenne_rating"]["value"]
print("Moyenne des ratings en base:", moyenne_rating)
