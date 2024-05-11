from  Cstsentiments import sentiments_positifs_fr,sentiments_negatifs_fr
import json
import re


jsonFile="../WonderboxFrance.json"
def convert_list_to_string(list):
    #print(list)
    # Check for None values and handle appropriately
    for element in list:
        if element is None:
            element = ""

    # Join the list elements into a string
    result_string = " ".join(list)
    return result_string

def neg_pos_fr_lexique(texte):
    # Initialiser une liste pour stocker les mots positifs détectés
    mots_positifs_detectes = []
    mots_negatifs_detectes = []


    # Parcourir chaque mot positif dans la liste

    # Parcourir chaque mot positif dans la liste
    for mot_positif in sentiments_positifs_fr:
        # Vérifier si le mot positif se trouve dans le texte
        if re.search(r'\b{}\b'.format(mot_positif), texte, flags=re.IGNORECASE):
            # Ajouter le mot positif à la liste des mots positifs détectés
            # Ajouter le mot positif à la liste des mots positifs détectés
            mots_positifs_detectes.append(mot_positif)

    # Parcourir chaque mot negatif dans la liste
    for mot_negatif in sentiments_negatifs_fr:
        # Vérifier si le mot positif se trouve dans le texte
        if re.search(r'\b{}\b'.format(mot_negatif), texte, flags=re.IGNORECASE):
            # Ajouter le mot positif à la liste des mots positifs détectés
            mots_negatifs_detectes.append(mot_negatif)


    return mots_negatifs_detectes,mots_positifs_detectes


with open(jsonFile, "r") as f:
    data = json.load(f)
# Envoyer les documents par lot pour optimiser les performances
for doc in data:
    commentaires_non_nuls = list(filter(lambda x: x is not None, doc["Commentaire"]))
    commentaire=convert_list_to_string(commentaires_non_nuls)
    print(commentaire)
    sentiment_by_sentence = neg_pos_fr(commentaire)
    mots_neg,mots_pos= neg_pos_fr(commentaire)
    print("Mots positifs:", mots_pos)
    print("Mots négatifs:", mots_neg)
