from textblob import TextBlob

# Texte à analyser
texte = "C'est une belle journée, mais le temps est vraiment mauvais, pas très bon."

# Créer un objet TextBlob avec le texte
blob = TextBlob(texte)

# Extraire les mots du texte
mots = blob.words

# Initialiser des listes pour les mots positifs et négatifs
mots_positifs = []
mots_negatifs = []

# Parcourir chaque mot et déterminer sa polarité
for mot in mots:
    polarite = TextBlob(mot).sentiment.polarity
    if polarite > 0:
        mots_positifs.append(mot)
    elif polarite < 0:
        mots_negatifs.append(mot)

# Afficher les mots positifs et négatifs
print("Mots positifs :", mots_positifs)
print("Mots négatifs :", mots_negatifs)