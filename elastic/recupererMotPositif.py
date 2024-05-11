import spacy
import json
from elasticsearch import Elasticsearch
from langdetect import detect_langs
from langdetect.lang_detect_exception import LangDetectException


# Charger le modèle de la langue française de spaCy
nlp = spacy.load("fr_core_news_sm")

# Texte contenant des mots positifs (exemple)
texte = "J'aime vraiment ce film, c'est fantastique et incroyable."
jsonFile = "WonderboxFrance.json"


# Detecter la langue du texte
def detect_language(commentaires):
    for commentaire in commentaires:
        try:
            print(commentaire)
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

# Retourner les mots negatifs ou positifs d'une phrase
def mots_pos_neg (comment):
    # Analyser le texte avec spaCy
    doc = nlp(comment)
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

    print("Mots positifs :", mots_positifs)
    print("Mots negatifs :", mots_negatifs)
    return (mots_positifs,mots_negatifs)

with open(jsonFile, "r") as f:
    data = json.load(f)

# Envoyer les documents par lot pour optimiser les performances
for doc in data:
    # Détecter la langue
    # Encode the text in UTF-8 (optional, but recommended)
    # Filtrer les commentaires non nuls

    commentaires_non_nuls = list(filter(lambda x: x is not None, doc["Commentaire"]))

    lang=detect_language(commentaires_non_nuls)
    print("Text=",commentaires_non_nuls,  " langue =", lang)

    comment=commentaires_non_nuls[0]

    if (lang != "no"):
        mots_positifs,mots_negatifs =  mots_pos_neg(comment)

        print("Mots positifs :", mots_positifs)
        print("Mots negatifs :", mots_negatifs)