import json
import spacy
jsonFile="../WonderboxFrance.json"
# Charger le modèle français de spaCy
nlp = spacy.load("fr_core_news_sm")
def convert_list_to_string(list):
    #print(list)
    # Check for None values and handle appropriately
    for element in list:
        if element is None:
            element = ""

    # Join the list elements into a string
    result_string = " ".join(list)
    return result_string

def neg_pos_fr(texte):
    # Analyser le texte avec spaCy
    doc = nlp(texte)

    # Initialiser des listes pour les mots positifs et négatifs
    mots_positifs = ""
    mots_negatifs = ""
    for token in doc:
    # Parcourir chaque token dans le document
    # Vérifier si le token est un adjectif

        if token.pos_ == "ADJ":
            print(token.text," ; ",token.sentiment)
            # Vérifier la polarité de l'adjectif
            if token.sentiment >= 0.5:  # Si le score de polarité est élevé, considéré comme positif
                mots_positifs=mots_positifs + token.text
            elif token.sentiment <= -0.5:  # Si le score de polarité est bas, considéré comme négatif
                mots_negatifs=mots_negatifs+token.text

    # Afficher les mots positifs et négatifs
    # print("Mots positifs :", mots_positifs)
    # print("Mots négatifs :", mots_negatifs)
    return(mots_negatifs,mots_positifs)

with open(jsonFile, "r") as f:
    data = json.load(f)
# Envoyer les documents par lot pour optimiser les performances
for doc in data:
    commentaires_non_nuls = list(filter(lambda x: x is not None, doc["Commentaire"]))
    commentaire=convert_list_to_string(commentaires_non_nuls)
    print(commentaire)
    sentiment_by_sentence = neg_pos_fr(commentaire)
    mots_pos,mots_neg= neg_pos_fr(commentaire)
    print("Mots positifs:", mots_pos)
    print("Mots négatifs:", mots_neg)
