-- 1. le nombre de pilotes de chaque nationalité (nationalité et nombre)
select dCountry, count(*) as 'nombre de pilotes'
from driver
group by dCountry
order by count(*) desc

-- 2. Même chose mais seulement pour les pilotes de course de la saison 2014
select dCountry, count(*) as 'nombre de pilotes'
from driver
    natural join racedriver
where rSeason = 2014
group by dCountry
order by count(*) desc, dCountry

-- 3. le nombre de points de chaque pilote en 2014 (nom, prenom, points), du meilleur au moins bon
select dFirstName, dLastName, sum(sPoints) as 'nombre de points'
from driver
    natural join standings
    natural join grandprix
where gDate like '2014%'
group by driverId
order by sum(sPoints) desc

-- 4. pour chaque grand prix de 2014, le nombre de pilotes classés (afficher « classé(s) »), disqualifiés (DQ), n’ayant pas pris le départ (DNS) et qui ont abandonné (DNF). Ces informations sont disponibles dans la colonne des « incidents de course ». Afficher le nom du grand prix (par ordre chronologique), le type de résultat et le nombre de pilotes concernés.
select gName, coalesce(sInc,'classé'), count(*) as 'nombre de pilotes concernés'
from grandprix
    natural join standings
where gDate like '2014%'
group by gName, sInc

-- 5. pour chaque pilote (nom, prénom), le nombre total de grands prix courus dans sa carrière (éventuellement 0)
select dFirstName, dLastName, count(gpId) as 'nombre de grand prix courus'
from driver
    natural left join standings
group by driverId
order by count(gpId) desc, dLastName, dFirstName

-- 6. le nombre de points de chaque équipe en 2014 (nom, points), de la meilleure à la moins bonne
select tName, sum(sPoints) as 'nombre de points'
from team
    natural join racedriver
    natural join driver
    natural join standings
where rSeason = 2014
group by teamId
order by sum(sPoints) desc

-- 7. [difficile / facultative] même chose, mais avec aussi le détail par pilote
select tName, case
	when driverId is null
    	then "Team"
  		else concat(dFirstName, " ", dLastName)
    end as 'Name', sum(sPoints) as 'nombre de points'
from team
    natural join racedriver
    natural join driver
    natural join standings
where rSeason = 2014
group by tname, driverId with rollup
-- pas d'order avec rollup, faire une sous requête

-- Exercice 2, requete avec sélections sur les agrégats
-- 1. les pays qui ont au moins 5 pilotes vivants (classés du pays qui a le plus de pilotes à celui qui en a le moins (on ne demande pas d’afficher combien il y en a)
select dCountry, count(*) - count(dDeathDate) as nbVivants
from driver
group by dCountry
having nbVivants >= 5
order by nbVivants desc

-- 2. les pilotes (prénom, nom) qui ont fait au moins 5 podiums en 2014
select dFirstName, dLastName, count(*)
from driver
    natural join standings
    natural join grandprix
where gDate like '2014%'
	and sPos < 4
group by driverId
having count(*) >= 5
order by count(*) desc

-- 3. les pilotes (prénom, nom) avec leur meilleur résultat en 2014, pour les pilotes qui ont fini au moins une fois « dans les points » (dans les 10 premiers) ; donner une version avec HAVING, et une version sans
select dFirstName, dLastName, min(sPos) as 'meilleur résultat'
from driver
    natural join standings
    natural join grandprix
where gDate like '2014%'
    and sPos < 11
group by driverId

-- avec having
select dFirstName, dLastName, min(sPos) as 'meilleur résultat'
from driver
    natural join standings
    natural join grandprix
where gDate like '2014%'
group by driverId
having min(sPos) < 11

-- 4. le nom des équipes dont au moins 2 pilotes (différents) ont fini sur le podium en 2014
select tName, count(distinct driverId) as 'nombre de pilotes sur le podium'
from team
    natural join racedriver
    natural join driver
    natural join standings
    natural join grandprix
where gDate like '2014%'
    and sPos < 4
group by teamId
having count(distinct driverId) >= 2

-- 5. les nationalités (de pilotes) pour lesquelles au moins 2 pilotes masculins sont décédés
select dCountry, count(dDeathDate) as 'nombre de pilotes décédés'
from driver
where dGender = 'M'
group by dCountry
having count(dDeathDate) >= 2
