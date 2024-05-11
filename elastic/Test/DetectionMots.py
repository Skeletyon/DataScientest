import json
import re
import nltk
from nltk.corpus import opinion_lexicon
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Cstsentiments  import sentiments_negatifs_fr,sentiments_positifs_fr
jsonFile="../WonderboxFrance.json"
pattern = r"\w+"  # Matches word characters

# Téléchargement des ressources si ce n'est pas déjà fait
nltk.download('punkt')
nltk.download('opinion_lexicon')
nltk.download('stopwords')

def check_word_in_list(phrase, emotions_list):
    """
    Check if a given word exists in a list of words.

    Args:
        word (str): The word to check.
        word_list (list): The list of words to search through.

    Returns:
        bool: True if the word exists in the list, False otherwise.
    """
    # Convert phrases to lowercase and split into words
 #   words1 = set(word.lower() for word in phrase1.split())


    # Ensure phrase1 is a string before using regular expressions
    if not isinstance(phrase, str):
        phrase = str(phrase)  # Convert to string if necessary
    words1 = re.findall(pattern, phrase)


    print(words1)
    print(emotions_list)

    emotions_set = set(word.lower() for word in emotions_list)

    # Extract common words (case-insensitive)

    common_words = (word.lower() for word in words1 if word.lower() in emotions_list)
    common_words_string = " ".join(common_words)


    return common_words_string

# Example usage
#
# negatives_emotions_list=""
# for emotion in sentiments_negatifs_fr:
#     negatives_emotions_list=negatives_emotions_list+","+emotion
#
# with open(jsonFile, "r") as f:
#     data = json.load(f)
# # Envoyer les documents par lot pour optimiser les performances
# for doc in data:
#     commentaires_non_nuls = list(filter(lambda x: x is not None, doc["Commentaire"]))
#     mots= check_word_in_list(commentaires_non_nuls, sentiments_positifs_fr)
#     print(f"The word '{mots}' is in the list.")

def recup_mot(phrase):


    # Téléchargement des ressources si ce n'est pas déjà fait
    nltk.download('punkt')
    nltk.download('opinion_lexicon')
    nltk.download('stopwords')

    # Charger les mots positifs et négatifs
    positive_words = set(opinion_lexicon.positive())
    negative_words = set(opinion_lexicon.negative())

    print(positive_words)
    print(negative_words)
    # Tokenisation de la phrase en mots individuels
    mots = word_tokenize(phrase.lower(), language='french')

    # Suppression des mots vides (stop words)
    mots = [mot for mot in mots if mot not in stopwords.words('french')]

    # Séparation des mots positifs et négatifs
    mots_positifs = [mot for mot in mots if mot in positive_words]
    mots_negatifs = [mot for mot in mots if mot in negative_words]

    print("Mots positifs :", mots_positifs)
    print("Mots négatifs :", mots_negatifs)
    return(mots_positifs,mots_negatifs)

def convert_list_to_string(list):
    print(list)
    # Check for None values and handle appropriately
    for element in list:
        if element is None:
            element = ""

    # Join the list elements into a string
    result_string = " ".join(list)
    return result_string

    # Function to analyze word-level sentiment within a sentence
def analyze_word_sentiment(phrase):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    # Initialize the sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Analyze sentiment by sentence
    sentence = analyzer.polarity_scores(phrase)

    positive_words = []
    for word in sentence.split():
        word_score = analyzer.polarity_scores(word)  # Analyze word individually
        if word_score['pos'] >= 0.5:  # Adjust the positivity threshold as needed
            positive_words.append(word)
    return positive_words


# Function to analyze sentiment of individual words (if per_sentence not available)
def analyze_word_sentiment_1(sentence):
  word_sentiments = []
  for word, score in analyzer.polarity_scores(sentence).items():
    word_sentiments.append((word, score))  # Combine word and its sentiment score
  return word_sentiments


  positive_words = [word for word, sentiment in word_sentiments if sentiment['pos'] >= 0.5]  # Filter positive words
  print(f"Positive words in sentence '{sentence}': {positive_words}")
# Téléchargement des ressources si ce n'est pas déjà fait
nltk.download('punkt')
nltk.download('opinion_lexicon')
nltk.download('stopwords')

with open(jsonFile, "r") as f:
    data = json.load(f)
# Envoyer les documents par lot pour optimiser les performances
for doc in data:
    commentaires_non_nuls = list(filter(lambda x: x is not None, doc["Commentaire"]))
    commentaire=convert_list_to_string(commentaires_non_nuls)
    print(commentaire)
    sentiment_by_sentence = analyze_word_sentiment_1(commentaire)
    # mots_pos,mots_neg= recup_mot(commentaire)
    print("Mots positifs:", mots_positifs)
    # print("Mots négatifs:", mots_neg)

    # Loop through sentences and identify positive words
    for sentence, score in sentiment_by_sentence.items():
        if 'per_sentence' not in dir(analyzer):  # Check if per_sentence is supported
            word_sentiments = analyze_word_sentiment(sentence)  # Analyze if necessary
        else:
            word_sentiments = [(word, score) for word, score in sentiment_by_word[sentence].items()]  # Access words from per-sentence results
    # Identifier les mots positifs
    mots_positifs = []
    for mot, score in sentiment_par_mot.items():
        if score['pos'] >= seuil_positivite:
            mots_positifs.append(mot)

    # Afficher les mots positifs
    print(f"Mots positifs : {mots_positifs}")