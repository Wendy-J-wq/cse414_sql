SELECT C.dest_city AS city
FROM (SELECT dest_city
      FROM FLIGHTS
      WHERE dest_city != 'Seattle WA'
      AND origin_city != 'Seattle WA') AS C
WHERE C.dest_city NOT IN (SELECT B.dest_city
                          FROM FLIGHTS AS A
                          JOIN FLIGHTS as B
                          ON A.dest_city = B.origin_city
                          OR A.dest_city = C.dest_city
                          WHERE A.origin_city = 'Seattle WA')
GROUP BY C.dest_city
ORDER BY C.dest_city ASC;

/* The result with 3 rows
Query succeeded | 175s

dest_city
Devils Lake ND
Hattiesburg/Laurel MS
St. Augustine FL
*/
