from datetime import datetime
import re
from dateutil.parser import parse

def detecter_format_date(date_str):
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

    print(date_str)

    for format_date in formats_possibles:
        try:
            date_obj = datetime.strptime(date_str, format_date)
            return format_date  # Retourne le format si l'analyse est réussie
        except ValueError:
            pass  # Passe au format suivant s'il y a une erreur de valeur

    return None  # Retourne None si aucun format n'a fonctionné


# Chaîne contenant la date
date_str = "12 avril 2024"
date_str_1="april 09 2024"
date_str2="2024-04-12"

# Détecter le format de date
format_date_detecte = detecter_format_date(date_str_1)

if format_date_detecte:
    print("Le format de date détecté est :", format_date_detecte)
else:
    print("Impossible de détecter le format de date.")