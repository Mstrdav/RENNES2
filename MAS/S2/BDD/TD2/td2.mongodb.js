use('sample_restaurants')

// 1. Donner la requête qui renvoie le nombre de restaurants français 1 de Manhattan qui ont eu au moins un contrôle depuis le 1er janvier 2014 (le résultat est 261). Même question depuis le 1er février 2014 (le résultat est 256). Peut-on en déduire le nombre de contrôles effectués en janvier ?
jan2014 = new Date('2014-01-01')
fev2014 = new Date('2014-02-01')

db.restaurants.find({
	"borough": "Manhattan",
	"cuisine": "French",
	"grades": {
		$elemMatch: {
			"date": {
				$gte: jan2014
			}
		}
	}
}).count()

db.restaurants.find({
	"borough": "Manhattan",
	"cuisine": "French",
	"grades": {
		$elemMatch: {
			"date": {
				$gte: fev2014
			}
		}
	}
}).count()

// 2. Donner maintenant la requête qui renvoie le nombre de restaurants français de Manhattan contrôlés en janvier 2014 (le résultat est 26). Noter que le champ date est dans un sous-document, et que le champ grades est une liste de sous-documents.
db.restaurants.find({
	"borough": "Manhattan",
	"cuisine": "French",
	"grades": {
		$elemMatch: {
			"date": {
				$gte: jan2014,
				$lt: fev2014
			}
		}
	}
}).count()

// 3. Donner la requête qui renvoie les restaurants français de Manhattan contrôlés le 6 janvier 2014 (il y en a 4). Peut-on répondre à la question avec un test d’égalité sur la date ? Pourquoi ? Si c’est possible, est-ce une bonne idée ?
jan62014 = new Date('2014-01-06')
jan72014 = new Date('2014-01-07')

db.restaurants.find({
	"borough": "Manhattan",
	"cuisine": "French",
	"grades": {
		$elemMatch: {
			"date": {
				$gte: jan62014,
				$lt: jan72014
			}
		}
	}
}).count()

// 4. Pour cette question, basculer sur la collection blog.posts de la base mas_test. Donner la requête qui renvoie les posts du 26 août 2015. Peut-on répondre à la question avec un test d’égalité sur la date ?
use('mas_test')
aug26_2015 = new Date('2015-08-26')
aug27_2015 = new Date('2015-08-27')

// on ne peut pas faire un test d'égalité parce que les dates sont précises à la seconde.
db['blog.posts'].find({
	"date": {
		$gte: aug26_2015,
		$lt: aug27_2015
	}
})

/**************************************
PARTIE 2 - Recherche avec et sans index
**************************************/
use('mas_large_db')

// 1. Donner la requête qui affiche les index disponibles sur la collection.
db.users.getIndexes()
db.users_index.getIndexes()

// 2. Donner la requête qui renvoie tous les documents pour lesquels l’utilisateur est user555, puis ré￾cupérer les informations suivantes : le nombre de documents renvoyés, le nombre de documents parcourus et le temps d’exécution de la requête.

// 3. Même question pour user499999.

// 4. On a pu constater que les 2 requêtes précédentes nécessitent le parcours complet de la collection. En effet, rien n’indique à MongoDB que les noms d’utilisateurs sont uniques et qu’il peut s’arrêter dès qu’il a trouvé LE document recherché. Par contre, on peut le faire côté utilisateur, soit en utilisant la méthode findOne() (mais comme elle ne renvoie pas un curseur, on ne peut lui appliquer explain()), soit en limitant le nombre de documents recherchés à 1 (ce qui revient au même). Reprendre les 2 questions précédentes en limitant la recherche à 1 seul document. Que peut-on en conclure sur le nombre moyen de documents examinés ?

// 5. Donner la requête qui renvoie les documents pour lesquels l’utilisateur a 55 ans, puis récupérer les informations suivantes : le nombre de documents renvoyés, le nombre de documents parcourus et le temps d’exécution de la requête.

// 6. Même question en triant les données par nom d’utilisateur croissant. Noter le surcoût dû au tri. Expliquer l’ordre obtenu sur les noms d’utilisateurs.

// 7. Donner la requête qui renvoie les documents pour les utilisateurs âgés de 5 à 114 ans, puis récupérer les informations suivantes : le nombre de documents renvoyés, le nombre de documents parcourus et le temps d’exécution de la requête.

// 8. Peut-on trier les résultats de cette requête ?

// 9. Même question pour les utilisateurs âgés de 20 à 24 ans.

// 10. Même question en triant les données par nom d’utilisateur croissant. Noter le surcoût dû au tri.