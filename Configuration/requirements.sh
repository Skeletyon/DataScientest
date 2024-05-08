#!/bin/bash
# Installez les librairies langdetect et pymongo
#apt-get install python3-pip

pip install spacy download

# Installez les modèles linguistiques spaCy pour l'anglais et le français
python -m spacy download en_core_web_sm
python -m spacy download fr_core_news_sm

#tail -f /dev/null