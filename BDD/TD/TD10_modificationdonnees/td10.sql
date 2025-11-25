-- 2.1 Ajout d'un grand prix
INSERT INTO grandprix VALUES (201501, "ROLEX AUSTRALIAN GRAND PRIX", 1, DATE('2015-03-17 17:00:00'), 58, 1); 

-- 2.2 Ajout de plusieurs grand prix
INSERT INTO grandprix (gpID, gName, circuitID, gDate, gLaps, gRank)
VALUES 
    (201502, 'PETRONS MALAYSIA GRAND PRIX', 2, DATE('2015-03-29 16:00:00'), 56, 2),
    (201503, 'UBS CHINESE GRAND PRIX', 4, DATE('2015-04-12 15:00:00'), 56, 3),
    (201504, 'GULF AIR BAHRAIN GRAND PRIX', 3, DATE('2015-04-19 18:00:00'), 57, 4);

