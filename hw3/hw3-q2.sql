SELECT DISTINCT F.origin_city AS city
FROM FLIGHTS as F
WHERE F.origin_city NOT IN
	(SELECT F1.origin_city
	 FROM FLIGHTS as F1
	 WHERE F1.actual_time >= 180)
	 AND F.canceled != 1
GROUP BY F.origin_city
ORDER BY F.origin_city ASC;

/* The result with 109 rows
Query succeeded | 12s

Output:
Aberdeen SD
Abilene TX
Alpena MI
Ashland WV
Augusta GA
Barrow AK
Beaumont/Port Arthur TX
Bemidji MN
Bethel AK
Binghamton NY
Brainerd MN
Bristol/Johnson City/Kingsport TN
Butte MT
Carlsbad CA
Casper WY
Cedar City UT
Chico CA
College Station/Bryan TX
Columbia MO
Columbus GA 
*/
