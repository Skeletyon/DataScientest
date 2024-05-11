from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd
from cleantext import clean
import datetime as dt

#Il faut aller sur la page gift shop pour recuperer le listing
url = 'https://www.trustpilot.com/categories/gift_shop?country=FR'


#pour ensuite aller sur le detail pour pouvoir recuperer les infos voulues
#ex: https://www.trustpilot.com/review/flashbay.fr
page = urlopen(url)
soup = bs(page, "html.parser")

#recuperer le nombre de pages d'avis
pages = soup.find('div', attrs={'class': 'styles_paginationWrapper__fukEb'})
pageTotal = pages.find()

lastPage = int(pageTotal.find('a', attrs={'name': 'pagination-button-last'}).text)
# lastPage=2

link_entreprise = []
nomEntreprise = []
nombreAvis = []
noteCompany = []
isVerifiedCompany = []
cinqEtoile = []
quatreEtoile = []
troisEtoile = []
deuxEtoile = []
uneEtoile = []



# Recuperation de toutes les entreprises de la categorie gift
for i in range(1, lastPage):
    urlUp = url  # Permet d'avoir une url de recherche toujours clean en debut de process
    # print(f"Page: {i}")
    if i != 1:  # Seule la premiere page n'a pas de ?page=x
        urlUp = url + '&page=' + str(i)

    # print(urlUp)
    page = urlopen(urlUp)
    soup = bs(page, "html.parser")
    # Il faut recuperer l'url du detail
    wonderboxDiv = soup.find('div', attrs={'class': 'styles_main__XgQiu'})
    values = wonderboxDiv.findAll('div', attrs={'class': 'paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_wrapper__2JOo2'})
    for record in values:

        # Trouvez l'élément <a> avec l'attribut href
        a_tag = record.find('a', href=True)

        # Récupérez la valeur de l'attribut href
        link_entreprise.append(a_tag.get('href'))

# print(link_entreprise)
# exit()
# Une fois qu'on a toutes les entreprises
for iterationNumber, entreprise_link in enumerate(link_entreprise, start=1):

    url_review = 'https://www.trustpilot.com' + entreprise_link
    # print(f"url_review: {url_review}, iterationNumber: {iterationNumber}")
    page = urlopen(url_review)

    soup = bs(page, "html.parser")
    wonderboxDiv = soup.find('div', attrs={'class': 'styles_summary__gEFdQ'})

    name = wonderboxDiv.find('span', attrs={'class': 'title_displayName__TtDDM'}).text.strip()
    print(name)
    nomEntreprise.append(name)

    avisNbr = wonderboxDiv.find('span', attrs={'class': 'styles_text__W4hWi'}).text[:-13].strip()
    nombreAvis.append(avisNbr)

    exist = wonderboxDiv.find('div', attrs={'class': 'typography_body-xs__FxlLP'})
    isVerified = 'oui' if exist and exist.text == 'VERIFIED COMPANY' else 'non'
    isVerifiedCompany.append(isVerified)

    ratingCompany = wonderboxDiv.find('p', attrs={'data-rating-typography': 'true'})
    noteCompany.append(ratingCompany)

    partieNote = soup.find('div', attrs={'class': 'styles_container__z2XKR'})

    partieCinqEtoile = partieNote.find('label', attrs={'data-star-rating': 'five'})
    fiveStar = partieCinqEtoile.find('p', attrs={'class': 'styles_percentageCell__cHAnb'}).text
    cinqEtoile.append(fiveStar)

    partieQuatreEtoile = partieNote.find('label', attrs={'data-star-rating': 'four'})
    fourStar = partieQuatreEtoile.find('p', attrs={'class': 'styles_percentageCell__cHAnb'}).text
    quatreEtoile.append(fourStar)

    partieTroisEtoile = partieNote.find('label', attrs={'data-star-rating': 'three'})
    threeStar = partieTroisEtoile.find('p', attrs={'class': 'styles_percentageCell__cHAnb'}).text
    troisEtoile.append(threeStar)

    partieDeuxEtoile = partieNote.find('label', attrs={'data-star-rating': 'two'})
    twoStar = partieDeuxEtoile.find('p', attrs={'class': 'styles_percentageCell__cHAnb'}).text
    deuxEtoile.append(twoStar)

    partieUneEtoile = partieNote.find('label', attrs={'data-star-rating': 'one'})
    oneStar = partieUneEtoile.find('p', attrs={'class': 'styles_percentageCell__cHAnb'}).text
    uneEtoile.append(oneStar)

dataEntreprise = pd.DataFrame(list(zip(
    nomEntreprise,
    noteCompany,
    isVerifiedCompany,
    nombreAvis,
    cinqEtoile,
    quatreEtoile,
    troisEtoile,
    deuxEtoile,
    uneEtoile
    )), columns=['Entreprise', 'Note', 'Entreprise verifiee', 'Nombre avis', '5', '4', '3', '2', '1'])
pd.set_option('display.max_columns', None)

json_df=dataEntreprise.to_json(orient="records",force_ascii=False)

current_date = dt.date.today()
f = current_date.strftime('%Y-%m-%d')
#Pour airflow
# nomFichier = "/opt/projet/scrapping/results/" + f + "_Wonderbox" + pays + ".json"
#pour du local
nomFichier = "./results/" + f + "_entreprises.json"

with open(nomFichier, "w",encoding='utf-8') as f:
    f.write(json_df)
f.close