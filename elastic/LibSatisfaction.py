import spacy
import datetime
from langdetect import detect_langs
from langdetect.lang_detect_exception import LangDetectException

#### IMPORTANT #######
# A charger : python -m spacy download en_core_web_sm
# A charger : python -m spacy download fr_core_news_sm


# Detecter la langue du texte
def detect_language(commentaires):
    for commentaire in commentaires:
        try:
            #print(commentaire)
            detected_langs = detect_langs(commentaire)
            if detected_langs:
                most_probable_lang = detected_langs[0]
                if most_probable_lang.prob > 0.5:
                    #print("Langue détectée pour le commentaire:", most_probable_lang.lang)
                    return( most_probable_lang.lang)
                else:
                    #print("Langue non détectée pour le commentaire.")
                    return("no")
            else:
                #print("Langue non détectée pour le commentaire.")
                return ("no")
        except LangDetectException:
            #print("Erreur de détection de la langue pour le commentaire.")
            return ("no")


# Charger le modèle de la langue française de spaCy
nlpFr = spacy.load("fr_core_news_sm")
# Charger le modèle de la langue anglaise de spaCy
# A charger : python -m spacy download en_core_web_sm
nlpEn = spacy.load("en_core_web_sm")
# Retourner les mots negatifs ou positifs d'une phrase
def mots_pos_neg (comment,lang):
    # Analyser le texte avec spaCy
    if (lang == "fr"):
        doc = nlpFr(comment)
    elif (lang == "en"):
        doc = nlpEn(comment)
    else:
        doc = nlpFr(comment)

    # Liste pour stocker les mots positifs
    mots_positifs = ""
    mots_negatifs = ""

    # Parcourir chaque token dans le document spaCy
    for token in doc:
        # Vérifier si le token est un adjectif et s'il est positif
        if token.pos_ == "ADJ":
            if token.dep_ == "advmod":
                # Ajouter le mot négatif à la liste des mots négatifs
                mots_negatifs = token.text + "," + mots_negatifs
            else:
                # Ajouter le mot positif à la liste des mots positifs
                mots_positifs = token.text + "," + mots_positifs

    #print("Mots positifs :", mots_positifs)
    #print("Mots negatifs :", mots_negatifs)
    mots_positifs = mots_positifs.rstrip(',')
    mots_negatifs = mots_negatifs.rstrip(',')

    return (mots_positifs,mots_negatifs)


def detect_format_date(date_str):
    formats_possibles = [
        "%d %B %Y",  # jour mois année (ex: 12 april 2024)
        "%B %d %Y",  # jour mois année (ex: april 12  2024)
        "%Y-%m-%d",  # année-mois-jour (ex: 2024-04-12)
        # Ajoutez d'autres formats possibles au besoin
    ]
    mois_fr_en = {
        "janvier": "January",
        "février": "February",
        "mars": "March",
        "avril": "April",
        "mai": "May",
        "juin": "June",
        "juillet": "July",
        "août": "August",
        "septembre": "September",
        "octobre": "October",
        "novembre": "November",
        "décembre": "December"
    }

    # Parcourir le dictionnaire et remplacer le mois français par son équivalent anglais
    for mois_fr, mois_en in mois_fr_en.items():
        if mois_fr in date_str:
            date_str = date_str.replace(mois_fr, mois_en)
            break  # Sortir de la boucle une fois que le mois a été remplacé



    for format_date in formats_possibles:
        try:
            date_obj = datetime.datetime.strptime(date_str, format_date)
            return date_str,format_date  # Retourne le format si l'analyse est réussie
        except ValueError:
            pass  # Passe au format suivant s'il y a une erreur de valeur

    return date_str,"None" # Retourne None si aucun format n'a fonctionné

def detect_sentiment_fr(phrase):
    from   textblob_fr  import PatternAnalyzer
    from textblob import TextBlob


    # Création d'un objet TextBlob avec l'analyseur PatternAnalyzer pour le français
    blob = TextBlob(phrase, analyzer=PatternAnalyzer())

    # Détection du sentiment
    sentiment = blob.sentiment

    # Vérification si le sentiment est négatif
    if sentiment[0] < 0:
#        print("negatif")
        return ("negatif")
    elif sentiment[0] == 0:
#       print("neutre")
        return("neutre")
    else:
#        print("positif")
        return("positif")


def detect_sentiment_other(phrase):
    from textblob import TextBlob

    # Création d'un objet TextBlob
    blob = TextBlob(phrase)

    # Détection du sentiment
    sentiment = blob.sentiment

    # Vérification si le sentiment est négatif
    if sentiment.polarity < 0:
        #print("negatif")
        return ("negatif")
    elif sentiment.polarity == 0:
        #print("neutre")
        return ("neutre")
    else:
        #print("positif")
        return("positif")

######################### Usage : Test LIB ###################################
# phrase="Le restaurant est bon.   Le menu, laccueil,  le service."
# detect_sentiment_fr(phrase)

# # #Texte contenant des mots positifs (exemple)
# texte = "J'aime vraiment ce film, c'est fantastique et incroyable."
# jsonFile = "satisfactionWonderbox.json"
#
# with open(jsonFile, "r") as f:
#     data = json.load(f)
#
# # Envoyer les documents par lot pour optimiser les performances
# for doc in data:
#     # Détecter la langue
#     # Encode the text in UTF-8 (optional, but recommended)
#     # Filtrer les commentaires non nuls
#
#     commentaires_non_nuls = list(filter(lambda x: x is not None, doc["Commentaire"]))
#
#     lang=detect_language(commentaires_non_nuls)
#     print("Text=",commentaires_non_nuls,  " langue =", lang)
#
#     comment=commentaires_non_nuls[0]
#
#     if (lang != "no"):
#         mots_positifs,mots_negatifs =  mots_pos_neg(comment,lang)
#
#         print("Mots positifs :", mots_positifs)
#         print("Mots negatifs :", mots_negatifs)

#
# # Chaîne contenant la date
# date_str = "12 avril 2024"
# date_str_1="Avril 09 2024"
# date_str2="2024-04-12"
#
# # Détecter le format de date
# format_date_detecte = detect_format_date(date_str_1)
# print(format_date_detecte)