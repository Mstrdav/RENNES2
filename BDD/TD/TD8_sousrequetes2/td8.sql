-- 1.1 our chaque grand prix de 2014, le nom du grand prix, le nombre de tours à parcourir, et l’écart par rapport au nombre de tours moyens des grands prix (de 2014)
select gName, gLaps, gLaps - (
  select avg(gLaps) from grandprix where gDate like '2014%'
)
from grandprix where gDate like '2014%'

-- 1.2 our chaque pilote de la saison 2014, le nombre de points qu’il a marqués, et le nombre de points de retard par rapport au premier, classés du premier au dernier
select driverID, (
  select max(total) as maximum
  from (
    select sum(Spoints) as somme
    from standings
    where gpID between 201401 and 201414
    group by driverID
  ) as c
) - sum(sPoints) as diff, sum(sPoints) as points
from standings
where gpID between 201401 and 201414
group by driverID
order by points desc
