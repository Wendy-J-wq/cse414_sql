SELECT B.dest_city AS city
FROM FLIGHTS AS A
JOIN (SELECT origin_city, dest_city
FROM FLIGHTS
WHERE dest_city != 'Seattle WA' AND
dest_city NOT IN
(SELECT dest_city from FLIGHTS
WHERE origin_city = 'Seattle WA')
GROUP BY origin_city, dest_city) AS B
ON A.dest_city = B.origin_city
WHERE A.origin_city = 'Seattle WA'
GROUP BY B.dest_city
ORDER BY B.dest_city ASC;

/* The result with 256 rows
Query succeeded | 37s

dest_city
Aberdeen SD
Abilene TX
Adak Island AK
Aguadilla PR
Akron OH
Albany GA
Albany NY
Alexandria LA
Allentown/Bethlehem/Easton PA
Alpena MI
Amarillo TX
Appleton WI
Arcata/Eureka CA
Asheville NC
Ashland WV
Aspen CO
Atlantic City NJ
Augusta GA
Bakersfield CA
Bangor ME
*/
