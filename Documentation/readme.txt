Créée le mardi 02 avril 2024

Pré-requis: Elasticsearch et Kibana installés.

1. Lancer le fichier scrapping.py .
	a. J'ai modifié le fichier srapping de Romain afin de récupérer les données dans 3 fichier JSON.
	# Écrit le fichier JSON
	with open("satisfactionWonderbox.json", "w",encoding='utf-8') as f:
		f.write(json_df)
	f.close


2. Créer 3 index dans Elasticsearch (creationindexStopWordFR.py,creationindexStopWordEN.py,creationindexStopWord.py)
-> Redéfinir les variables url, user, password selon votre environnement.
-> Pour modifier le password, 2 manières de le faire:
	- Avec une ligne de commande, par exemple : bin/elasticsearch-reset-password --username elastic
	- A partir de Kibana :  dans la console de developpement
		PUT /api/security/users/<nom_utilisateur>
		{
		  "password": "<nouveau_mot_de_passe>"
		}
3. Définir un mapping (schéma) de l'index (avec un analyzer français , par exemple) => lancer creationIndexStopWord.py etc
4. Tester l'existence de l'index après la création (testindex.py)

5. Lancvement du chargement de données. (chargement.py)

6. Faire de requêtes (query.py)


Remarques: Les fichiers python à récupérer et à exécuter dans l'ordre
- scrapping.py --> Vérifier la création des 3 fichiers json
- creationIndexStopWord.py
- creationIndexStopWordEN.py
- creationIndexStopWordFR.py
- chargement.py
