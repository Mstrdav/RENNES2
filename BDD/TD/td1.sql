-- Nom des circuits
select cName from circuit

-- Nom, prénom et date de naissance des pilotes
select dFirstName, dLastName, dBirthDate from driver

-- La table team complète
select * from team

-- Les pays des pilotes (avec, puis sans doublons)
select dCountry from driver
-- sans doublon
select distinct dCountry from driver

-- Les points attribués (sans doublons)
select distinct sPoints from standings

-- drivers français (prénom, nom, date de naissance)
select distinct dFirstName, dLastName, dBirthdate from driver where dCountry = 'France'

-- selectionne circuits compris entre 4 et 5 km
select distinct cName, cCity, cLength from circuit where cLength < 5 and cLength >= 4
select distinct cName, cCity, cLength from circuit where cLength between 4 and 5

-- francais nés avant 1990
select distinct dFirstName, dLastName, dbirthdate from driver where dcountry = 'France' and dbirthdate < '1990-01-01'

-- pilotes français, belges ou suisse, de deux manières différentes
select dfirstname, dlastname from driver where dcountry in ('France', 'Belgium', 'Switzerland')
select dfirstname, dlastname from driver where dcountry = 'France' or dcountry = 'Belgium' or dcountry = 'Switzerland'

-- Pilotes dont les noms commencent par M
select dfirstname, dlastname, dcountry from driver where dlastname like 'M%'
select dfirstname, dlastname, dcountry from driver where substring(dlastname, 1, 1) = 'M'
select dfirstname, dlastname, dcountry from driver where left(dlastname, 1) = 'M'

-- Pilotes dont les noms commencent par M mais pas par Me
select dfirstname, dlastname, dcountry from driver where regexp_like(dlastname, 'M[a-df-z]?') -- interdit
select dfirstname, dlastname, dcountry from driver where dlastname like 'M%' and not dlastname like 'Me%'

-- Les noms de circuits qui ne comportent pas le mot circuit
select cname from circuit where cname not like '%circuit%'

-- circuit sans record
select cname, ccity, claprec from circuit where claprec is Null

-- morts
select dfirstname, dlastname from driver where ddeathdate is not Null

-- drivers hommes nés entre x et y avec des noms
select dfirstname, dlastname, dcountry, dbirthdate from driver where dgender = 'M' and left(dlastname,1) in ('B','P') and dbirthdate between '1985-01-01' and '1991-12-31'

-- pilotes allemands alphabétique
select dlastname, dfirstname  from driver where dcountry = 'Germany' order by dlastname, dfirstname

-- les pilotes du plus jeune au plus vieux
select dlastname, dfirstname  from driver order by dbirthdate desc

-- pareil par nationalité et nom
select dlastname, dfirstname, dcountry, dbirthdate from driver order by dcountry, dlastname

-- un tri chelou
select * from standings order by driverid, spos, gpid desc

/*
Exprimer en français les informations que renvoient les requêtes suivantes :

1. SELECT *
    FROM circuit
    WHERE cLapRec <= 90
    ORDER BY cLength DESC

-> affiche la table des circuits comptabilisant un record de moins de 90 secondes au tour, du plus grand circuit au plus court.

2. SELECT dFirstName, dLastName, dCountry
    FROM driver
    WHERE dBirthdate BETWEEN '1985-01-01' AND '1992-12-31'
    AND dDeathDate IS NULL
    AND dCountry IN ('Germany', 'Netherlands', 'Switzerland')
    ORDER BY dCountry, dLastName

-> affiche prénom, nom et nationalité des pilotes allemands, néerlandais ou suisse, nés entre 85 et 92, toujours vivant, triés par pays et par ordre alphabétique (nom de famille)
*/

-- 10 premiers drivers par id
select driverID, dFirstName, dlastname from driver order by driverid limit 10

-- la meme mais que le 6, 7 et 8
select driverID, dFirstName, dlastname from driver order by driverid limit 3 offset 6
select driverID, dFirstName, dlastname from driver order by driverid limit 5,3