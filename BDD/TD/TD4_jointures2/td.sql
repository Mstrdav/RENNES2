-- Exercice 1
-- 1. Cette requête renvoie les correspondances entre les anciens et nouveaux noms d'une équipe

-- 2. Cette requete associe chaque pilote à tous les pilotes plus jeunes ou de même age

-- Exercice 2
-- 1. Les noms et prénoms des pilotes qui ont actuellement un record du tour sur un circuit de leur pays, par ordre alphabétique.
select dLastName, dFirstName
from driver 
    join circuit on driverID = cDrivRec and dCountry = cCountry
order by dLastName

-- 2. Les circuits (nom, ville, longueur), plus courts que le « Hungaroring », du plus long au plus court (on suppose que dans l’écriture de la requête on ne connait pas a priori la longueur du Hungaroring, mais seulement son nom)
select cName, cCity, cLength
from circuit
where cLength < (select cLength from circuit where cName = 'Hungaroring')
order by cLength desc

-- Version autojointure
select c1.cName, c1.cCity, c1.cLength
from circuit c1
    join circuit c2 on c1.cLength < c2.cLength and c2.cName = 'Hungaroring'
order by c1.cLength desc

-- 3. Les doublets de pilotes (nom1, nom2) qui ont même prénom et même nationalité (pour éviter des redondances ou d’associer un pilote à lui-même, on peut ajouter une condition d’inégalité sur les identifiants).
select distinct d1.dFirstName, d1.dCountry
from driver d1
    join driver d2 on d1.dFirstName = d2.dFirstName
        and d1.dCountry = d2.dCountry
        and d1.driverID <> d2.driverID

-- 4. Les pilotes qui courent pour une équipe étrangère en 2014 (nom, prénom du pilote, nom de l’équipe).
select dLastName, dFirstName, tName
from driver 
    join racedriver
    join team on racedriver.driverID = driver.driverID 
    and racedriver.teamID = team.teamID
    and rSeason = 2014
    and dCountry <> tCountry

-- 5. Toutes les associations pilote de course (nom, prénom) / pilote d’essai (nom, prénom) de la même équipe pour la saison 2014
select d1.dLastName as "rLastName", d1.dFirstName as "rFirstName", d2.dLastName as "tLastName", d2.dFirstName as "tFirstName"
from driver d1
    join racedriver on d1.driverID = racedriver.driverID and rSeason = 2014
    join team on racedriver.teamID = team.teamID
    join testdriver on team.teamID = testdriver.teamID and tSeason = 2014
    join driver d2 on testdriver.driverID = d2.driverID

-- Exercice 3 (jointures externes, conserver toutes les lignes)
-- 1. tous les circuits des grands prix de 2014 (ville, date du grand prix) avec le nom du recordman du tour, lorsqu’il est connu, en présentant les résultats par ordre chronologique
select cCity, gDate, dLastName
from grandprix
    natural join circuit
        left join driver on cDrivRec = driverID
            and gDate like '2014%'
order by gDate desc

-- 2. tous les grands prix de 2014 (nom, date) avec, lorsqu’il est connu, le nom du vainqueur, dans l’ordre chronologique
select gName, gDate, dLastName
from grandprix
    natural join standings
    left join driver on standings.driverID = driver.driverID
        and sPos = 1
        and gDate like '2014%'
order by gDate desc

-- 3. pour chaque pilote (prénom, nom, date de naissance), les grands prix (nom, date) qui ont eu lieu le jour de son anniversaire, et NULL s’il n’y en a pas, dans l’ordre alphabétique des pilotes Remarque : la fonction MONTH(<date>) (resp. DAY(<date>))) permet d’extraire le mois (resp. le jour) d’une date.
select dFirstName, dLastName, dBirthDate, gName, gDate
from driver
    left join grandprix on MONTH(dBirthDate) = MONTH(gDate) and DAY(dBirthDate) = DAY(gDate)
order by dLastName, dFirstName

-- Exercice 4
-- 1. les équipes (nom) qui n’ont jamais eu de pilote d’essai
select tName
from team
    left join testdriver on team.teamID = testdriver.teamID
where testdriver.teamID is null

-- 2. les pilotes (nom, prénom) qui n’ont jamais été pilote de course, dans l'ordre alphabétique
select dLastName, dFirstName
from driver
    natural left join racedriver
where racedriver.driverID is NULL

-- Exercice 5
-- 1. Pour chaque pilote (nom, prénom), les grand-prix (nom, date) qu'il a gagné, NULL s'il n'a jamais gagné de grand-prix, trié par pilote et par date de grand-prix

-- 2. Tous les pilotes (nom, prenom) qui n'ont jamais été classé, qui n'ont jamais participé à un grand-prix, par ordre alphabétique