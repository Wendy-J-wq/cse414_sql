SELECT F2.origin_city,
ISNULL((SELECT COUNT(*)
       FROM FLIGHTS AS F1
       WHERE F1.origin_city = F2.origin_city
       AND F1.actual_time < 180
       AND F1.canceled != 1
       GROUP BY F1.origin_city)*100.00/COUNT(*),0) AS percentage
FROM FLIGHTS AS F2
WHERE F2.canceled != 1
GROUP BY F2.origin_city
ORDER BY percentage ASC, F2.origin_city ASC;

/* The result with 327 rows
Query succeeded | 10s

origin_city	percentage
Guam TT	0.0000000000000
Pago Pago TT	0.0000000000000
Aguadilla PR	28.8973384030418
Anchorage AK	31.8120805369127
San Juan PR	33.6605316973415
Charlotte Amalie VI	39.5588235294117
Ponce PR	40.9836065573770
Fairbanks AK	50.1165501165501
Kahului HI	53.5144713526284
Honolulu HI	54.7390288236821
San Francisco CA	55.8288645371881
Los Angeles CA	56.0808908229873
Seattle WA	57.6093877922314
Long Beach CA	62.1764395139989
New York NY	62.3718341367280
Kona HI	63.1607929515418
Las Vegas NV	64.9202563720375
Christiansted VI	65.1006711409395
Newark NJ	65.8499710969807
Plattsburgh NY	66.6666666666666
*/
