SELECT DISTINCT F.origin_city, F.dest_city, F.actual_time AS time
FROM FLIGHTS AS F
JOIN (SELECT origin_city, MAX(actual_time) as max_time
      FROM FLIGHTS
      GROUP BY origin_city) AS C
ON F.origin_city = C.origin_city
AND F.actual_time = C.max_time
ORDER BY F.origin_city ASC, F.dest_city ASC;

/* The result with 334 rows
Query succeeded | 19s

origin_city	dest_city	time
Aberdeen SD	Minneapolis MN	106
Abilene TX	Dallas/Fort Worth TX	111
Adak Island AK	Anchorage AK	471
Aguadilla PR	New York NY	368
Akron OH	Atlanta GA	408
Albany GA	Atlanta GA	243
Albany NY	Atlanta GA	390
Albuquerque NM	Houston TX	492
Alexandria LA	Atlanta GA	391
Allentown/Bethlehem/Easton PA	Atlanta GA	456
Alpena MI	Detroit MI	80
Amarillo TX	Houston TX	390
Anchorage AK	Barrow AK	490
Appleton WI	Atlanta GA	405
Arcata/Eureka CA	San Francisco CA	476
Asheville NC	Chicago IL	279
Ashland WV	Cincinnati OH	84
Aspen CO	Los Angeles CA	304
Atlanta GA	Honolulu HI	649
Atlantic City NJ	Fort Lauderdale FL	212
*/
