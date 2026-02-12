use mas_etudiants

// etudians mineurs
db.licence.find({"age": {$lt: 18}}, {"nom": true, "prénom": true})

// etudiants agés de 20 à 22 ans, de deux façons différentes
db.licence.find({"age": {$in: [20, 21, 22]}}, {"nom": true, "prénom": true})
db.licence.find({$and: [{"age": {$gte: 20}}, {"age": {$lte: 22}}]}, {"nom": true, "prénom": true})

// etudiants agés strictement de moins de 20 ou de plus de 22 ans
db.licence.find({$or: [{"age": {$lt: 20}}, {"age": {$gt: 22}}]}, {"nom": true, "prénom": true})

// etudiants de moins de 22 ans, soit L1 MIASHS, soit pas L1 pas MIASHS
db.licence.find({
	"age": {$lte: 22},
	$or: [
		{"année": 1, "discipline": "MIAS"},
		{"année": {$ne: 1}, "discipline": {$ne: "MIAS"}}
	]
})

// etudiant sans sexe ni prénom
db.licence.find({
	"prénom": null,
	"sexe": null
})

// etudiants soit sans sexe soit sans prenom, mais pas les deux
db.licence.find({
	$or: [
		{"sexe": null, "prénom": {$ne: null}},
		{"prénom": null, "sexe": {$ne: null}}
	]
})

// etudiant (nom prenom discipline) de sciences sociales
db.licence.find(
	{"discipline": {$in: ["GEOG", "MIAS", "AESO", "HIST"]}},
	{"nom": true, "prénom": true, "discipline": true}
)

