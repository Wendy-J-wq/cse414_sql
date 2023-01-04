SELECT DISTINCT M.name AS carrier
FROM (SELECT *
      FROM FLIGHTS AS F
      JOIN CARRIERS AS C
      ON C.cid = F.carrier_id) AS M
WHERE M.origin_city = 'Seattle WA'
AND M.dest_city = 'San Francisco CA'
ORDER BY carrier ASC;

/* result with 4 rows
Query succeeded | 31s

carrier
Alaska 	Airlines 	Inc.
SkyWest	 Airlines	 Inc.
United 	Air Lines	 Inc.
Virgin 	America
/*
