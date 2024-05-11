import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import wordnet as wn

nltk.download('wordnet')
nltk.download('vader_lexicon')  # Download VADER lexicon for sentiment analysis
nltk.download('omw-1.4')

# Create VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

verbes = nltk.corpus.wordnet.words()
#verbes = nltk.corpus.worlnet.all_verbs()
verbes_positifs = []
verbes_negatifs = []
verbes_neutres = []

for verbe in verbes:
    # Convert word to lowercase for case-insensitive sentiment analysis
    word_lower = verbe.lower()

    # Use VADER to analyze sentiment of the word
    sentiment = analyzer.polarity_scores(word_lower)
    #print(sentiment)
    # Check if sentiment is positive (polarity > 0)
    if sentiment['pos'] > 0:
        verbes_positifs.append(verbe)
    elif sentiment['neg'] > 0:
        verbes_negatifs.append(verbe)
    else:
        verbes_neutres.append(verbe)

# Print the first 10 positive verbs
print(len(verbes_positifs))
print(len(verbes_negatifs))
print(len(verbes_neutres))

print(verbes_positifs[:10])
print(verbes_negatifs[:10])
print(verbes_neutres[:10])




# Fonction pour obtenir les verbes positifs en français
def get_positive_verbs():
    positive_verbs = []
    for synset in wn.all_synsets('v'):
        for lemma in synset.lemmas(lang='fra'):
            #print(lemma.name())
            if lemma.antonyms():
                continue
            positive_verbs.append(lemma.name())
    return positive_verbs

# Obtenir la liste des verbes positifs en français
positive_verbs = get_positive_verbs()

# Afficher les 10 premiers verbes positifs en français
print("Les 10 premiers verbes positifs en français :")
print(positive_verbs[:100])