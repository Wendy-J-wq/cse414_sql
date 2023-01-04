SELECT DISTINCT C.name as carrier
FROM FLIGHTS AS F
JOIN CARRIERS AS C
ON C.cid = F.carrier_id
WHERE F.origin_city = 'Seattle WA' AND
F.dest_city = 'San Francisco CA'
ORDER BY carrier ASC;

/* result with 4 rows
Query succeeded | 18s

carrier
Alaska 	Airlines 	Inc.
SkyWest	 Airlines	 Inc.
United 	Air Lines	 Inc.
Virgin 	America
/*
