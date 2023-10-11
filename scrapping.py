from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd

url = 'https://www.trustpilot.com/review/www.wonderbox.fr'  # ?page=2
page = urlopen(url)

soup = bs(page, "html.parser")


#recuperer le nombre de pages d'avis
pages = soup.find('div', attrs={'class': 'styles_pagination__6VmQv'})
pageTotal = pages.find()
# print(pages.prettify())S

lastPage = int(pageTotal.find('a', attrs={'name': 'pagination-button-last'}).text)
# print(lastPage)
# exit()
personne = []
# commentTitle = []
commentaire = []
date = []
rating = []
reply = []
for i in range(1, lastPage):
    if i != 1 : #La premiere page n'a pas de ?page=x
        url = 'https://www.trustpilot.com/review/www.wonderbox.fr'  # ?page=2
        page = urlopen(url)
        soup = bs(page, "html.parser")

    # Recuperer tous les avis de la page
    avis = soup.findAll('div', attrs={'class': 'styles_reviewCardInner__EwDq2'})

    for record in avis:
        fullCommentaire = []
        title = record.find('div', attrs={'class': "styles_consumerDetailsWrapper__p2wdr"})
        # print(record)
        note = record.find('div', attrs={'class' : "star-rating_starRating__4rrcf star-rating_medium__iN6Ty"})

        if note is not None:
            note = note.img.get("src")[-5]

        rating.append(note)
        if title is not None:
            nom_prenom = title.find('span',
                                attrs={'class': 'typography_heading-xxs__QKBS8 typography_appearance-default__AAY17'}).text
        else:
            nom_prenom = "test"

        personne.append(nom_prenom)
        globalAvis = record.find('div', {'class': 'styles_reviewContent__0Q2Tg'})
        # print(globalAvis)
        if globalAvis is not None:
            avisDetaille = globalAvis.p.text

        commentaireAvis = record.find('p', {'class': 'typography_body-l__KUYFJ'})
        commentTitle = record.find('h2', {'class': 'typography_heading-s__f7029'})
        commentTitleText = commentTitle.text if commentTitle is not None else 'None'
        # print(commentTitleText)

        # first = 0 if pointer1.data is None else pointer1.data

        if commentaireAvis is not None:
            fullCommentaire.append(commentaireAvis.text)
        else:
            fullCommentaire.append('None')

        dateAvis = record.find('p', attrs = {'class': 'typography_body-m__xgxZ_'})
        if dateAvis is not None:
            dateFormat = dateAvis.text.replace('Date of experience: ', '')
        else:
            dateFormat = "None"
        date.append(dateFormat)

        #construction de l'objet commentaire
        fullCommentaire.append(commentTitle)
        commentaire.append(fullCommentaire)
        # replyBox = record.find('p', {'class' : 'styles_message__shHhX'})
        replyBox = record.find('div', attrs = {'class' : 'paper_paper__1PY90'})

        if replyBox is not None:
            # print(replyBox.prettify())
            dateReponse = replyBox.find('time', attrs = {'class' : 'typography_body-m__xgxZ_'})
            responseText = replyBox.find('p', {'class' : 'styles_message__shHhX'}).text
            responseFrom = replyBox.find('p', {'class' : 'styles_replyCompany__ro_yX'}).text
            response = [responseFrom, dateReponse, responseText]
        else:
            response = 'None'
        reply.append(response)

avis_col = pd.DataFrame(list(zip(personne, commentaire, rating, date, reply)), columns=['Personne', 'Commentaire', 'Rating', 'Date', 'Reponse'])
# print(avis_col.iloc[3])
avis_col.to_json('resultat.json')
