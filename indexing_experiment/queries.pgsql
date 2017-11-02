EXPLAIN ANALYZE SELECT * FROM ZipCodeRange  
    WHERE earth_box(ll_to_earth(52.3667, 4.9000), 100) @> ll_to_earth(latitude, longitude)
    LIMIT 100