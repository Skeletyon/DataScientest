from textblob_fr import PatternAnalyzer
from textblob  import TextBlob
# Phrase à analyser
phrase = "Le produit est rapide"

# Création d'un objet TextBlob avec l'analyseur PatternAnalyzer pour le français
blob = TextBlob(phrase, analyzer=PatternAnalyzer())

# Détection du sentiment
sentiment = blob.sentiment

# Vérification si le sentiment est négatif
if sentiment[0] < 0:
    print("Sentiment négatif détecté.")
else:
    print("Pas de sentiment négatif détecté.")