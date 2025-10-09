select * from circuit 
inner join driver on cDrivRec = driverID

select * from circuit
inner join driver on cDrivRec = driverID
where cLength > 5

select * from circuit
inner join driver on cDrivRec = driverID
where cLength > 5
order by dLastName, cYearRec DESC, cLength DESC

select dLastName, dFirstName, cName, cCity, cYearRec, cLapRec from circuit
inner join driver on cDrivRec = driverID
where cLength > 5
order by dLastName, cYearRec DESC, cLength DESC

select gName, gDate, cLength, gLaps 
from grandprix join circuit on grandprix.circuitID = circuit.circuitID
where gpID DIV 100 = 2014 
order by gDate

-- ou
select gName, gDate, cLength, gLaps 
from grandprix natural join circuit
where gpID DIV 100 = 2014 
order by gDate

-- ou
select gName, gDate, cLength, gLaps 
from grandprix join circuit using(circuitID)
where gpID DIV 100 = 2014 
order by gDate

-- celle-ci peut se faire des trois façons comme la précédente
select dLastName, dFirstName, rDriverNb
from racedriver natural join driver
where rSeason = 2014
order by rDriverNb

-- celle-ci ne peut pas se faire naturellement car les attributs n'ont pas le meme nom
select distinct dLastName, dFirstName
from driver join circuit on driverID = cDrivRec
order by dLastName, dFirstName

select distinct dLastName, dFirstName, rDriverNb, tName
from racedriver 
	natural join driver
    natural join team
order by tName, rDriverNb

-- pfiouuuh
select distinct cCountry, gName, dLastName, tName 
from (
  	select * from grandprix natural join standings 
	where sPos = 1 and gpID div 100 = 2014 
) as gpclass
	natural join driver
	natural join racedriver
    natural join team
    natural join circuit
order by gDate

-- pour chaque grand prix de 2014, le nom du grand prix, la ville du circuit, le temps du record du tour et les prénom et nom du pilote recordman, dans l’ordre alphabétique des villes
select gName, cCity, cLapRec, dFirstName, dLastName
from grandprix
    natural join circuit
    natural join driver
where gpID div 100 = 2014