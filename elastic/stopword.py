import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
print(stopwords.words('english'))
print(stopwords.words('french'))
print(stopwords.words('dutch'))

