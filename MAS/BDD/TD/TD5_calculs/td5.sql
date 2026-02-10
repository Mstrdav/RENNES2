-- 1.1
select cName, gLaps, cLength
from grandprix
natural join circuit
where gDate like '2014%'
order by gDate

-- 1.2
select gName as 'Grand prix', concat(substr(dFirstName, 1,1), ". ", dLastName) as 'Vainqueur'
from grandprix
natural join standings
natural join driver
where gDate like '2014%'
	and sPos = 1

-- 1.3
select dLastName, dFirstName, dBirthDate, Round(DATEDIFF(coalesce(dDeathDate,CURRENT_DATE()), dBirthDate)/365.2425) as age
from driver
order by age desc

-- 1.4
select dLastName, dFirstName, dBirthDate, Round(DATEDIFF(CURRENT_DATE(), dBirthDate)/365.2425) as age
from driver where dDeathDate is null
order by age desc

-- 1.5
select dLastName, dFirstName, Round(DATEDIFF(coalesce(dDeathDate,CURRENT_DATE()), dBirthDate)/365.2425) as 'durée de vie'
from driver
where dDeathDate is not null
order by dLastName, dFirstName desc

-- 1.6 -> c'est ce que j'ai fait à la 3

-- 2.1
select avg(gLaps), sum(gLaps)
from grandprix
where gDate like '2014%'

-- 2.2
select min(gLength)
from grandprix like '2014%'

-- 2.3 peut-on afficher de manière simple le circuit correspondant ?
select cName, gLength
from grandprix
natural join circuit
where gLength = (select min(gLength) from grandprix like '2014%') -- c'est pas si simple, puisqu'on est obligé de faire une sous-requête

-- 2.4
select year(min(dBirthDate)) as 'Naissance du plus vieux', year(max(dBirthDate)) as 'Naissance du plus jeune'
from racedriver
    natural join driver
where dDeathDate is null
    and rSeason = 2014

-- 2.5
select count(*) as 'Nombre de courses en 2014'
from grandprix
where gDate like '2014%'

-- 2.6
select count(*) as 'Nombre de pilotes vivants nés avant 1950'
from driver
where dDeathDate is null
    and year(dBirthDate) < 1950

-- 2.7.1
select count(*)
from driver
where dDeathDate is not null

-- 2.7.2
select count(dDeathDate)
from driver

-- nombres de pilotes vivants
select count(*) -  count(dDeathDate)
from driver

-- 2.8
select count(*)
from driver
    natural join standings
    natural join grandprix
where sPos = 1
    and gDate like '2014%'