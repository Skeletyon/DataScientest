import re

# Liste des mots positifs
sentiments_positifs_fr = [
    "joie",
    "bonheur",
    "amour",
    "gratitude",
    "satisfaction",
    "confiance",
    "espoir",
    "sérénité",
    "paix"
]

# Texte à analyser
texte = "La joie et le bonheur sont des sentiments merveilleux."

# Initialiser une liste pour stocker les mots positifs détectés
mots_positifs_detectes = []

# Parcourir chaque mot positif dans la liste
for mot_positif in sentiments_positifs_fr:
    # Utiliser une expression régulière pour rechercher le mot positif dans le texte
    if re.search(r'\b{}\b'.format(mot_positif), texte, flags=re.IGNORECASE):
        # Ajouter le mot positif à la liste des mots positifs détectés
        mots_positifs_detectes.append(mot_positif)

# Afficher les mots positifs détectés
print("Mots positifs détectés :", mots_positifs_detectes)