from elasticsearch import Elasticsearch
from langdetect import detect_langs
from langdetect.lang_detect_exception import LangDetectException

import json

# Définir l'URL de la base Elasticsearch
url = "http://localhost:9200"

# Définir le nom d'utilisateur et le mot de passe
username = "elastic"
password = "changeme"
jsonFile = "satisfactionWonderbox.json"
indexname= "satisfactionclients"

es = Elasticsearch(
        url,
        basic_auth=(username, password),

    )

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

# Exemple d'utilisation
#commentaires_non_nuls = ["J'ai un coupon de réduction qui n' jamais voulu marcher"]



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