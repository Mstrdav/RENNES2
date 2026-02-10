-- Exercice 1. Sous-requêtes corrélées
-- Donner les requêtes SQL qui renvoient les informations suivantes :

-- 1. les pilotes (nom, prénom) dans l’ordre alphabétique, avec leur meilleur résultat (place), et le circuit sur lequel il a été réalisé (nom, pays) pour la saison 2014 ; si ce meilleur résultat a été réalisé sur plusieurs grands prix (eg. plusieurs victoires), donner tous les circuits (1 par ligne) dans l’ordre chronologique des grands prix
select dLastName, dFirstName, sPos, gName, cCountry
from driver
    natural join standings
    natural join grandprix
    natural join circuit
where sPos = (
    select min(sPos)
    from standings
    where driverID = driver.driverID
    and gpID like '2014%'
)
    and gDate like '2014%'
order by dLastName, dFirstName, gDate;

-- 2. pour chaque pilote (nom, prénom), le nombre d’années depuis sa dernière victoire (en supposant la BD plus complète qu’elle n’est réellement...)
select dLastName, dFirstName, min(year(now()) - year(gDate)) as years_since_last_win
from driver
    natural join standings
    natural join grandprix
where sPos = 1
group by driverID
order by dLastName, dFirstName; -- oui j'ai pas fait de sous requete :'(

-- 3. les pilotes (nom, prénom) qui n’ont jamais été au delà de la 10e place sur la grille de départ d’un grand prix en 2014 (en utilisant EXISTS)
select dLastName, dFirstName
from driver
where not exists (
    select *
    from standings
        natural join grandprix
    where standings.driverID = driver.driverID
        and gDate like '2014%'
        and sGrid > 10
)

-- Exercice 2. Division
-- Donner les requêtes SQL qui renvoient les informations suivantes :

--1. les pilotes (nom, prénom) qui ont fini les 8 premiers grands prix de 2014 dans les points (= dans les 10 premières places)
select dLastName, dFirstName
from driver
    where not exists (
        select *
        from standings s1
        where s1.gpID < '201409'
            and (
                (s1.sPos > 10 and s1.driverID = driver.driverID)
                or
                not exists (
                    select *
                    from standings s2
                    where s1.gpID = s2.gpID
                        and s1.driverID = driver.driverID
                )
            )
    )
order by dLastName, dFirstName;

-- 2. le nom des équipes qui ont placé (au moins) un pilote sur le podium de chaque course (dont on connait les résultats) en 2014
select distinct tName
from team
