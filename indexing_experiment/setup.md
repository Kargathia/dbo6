# Indexing comparison experiment

This experiment seeks to verify and measure the impact of some of the theoretical advantages when using different indexing strategies.

## Casus

The ZipcodeRange table in the Zipcode database has latitude and longitude properties. When performing the basic query "find me zip code ranges within XXX distance of longitude X and latitude Y, sort by distance", the database performs a set of 2D comparison operators.

According to their descriptions, R-trees are well-suited to making 2D or 3D comparisons. We can test this assertion relatively simple, using the Zipcode database.

In the experiment, we can do a three-way comparison. We compare table columns that are:
- Not indexed
- Indexed with a B-Tree strategy
- Indexed with a R-Tree strategy

## Hypothesis

Based on theoretical properties of B and R Trees, we'd expect that the R-Tree has the biggest positive effect on the query, followed by the B-Tree.
A non-indexed table is expected to be slower than either indexing method.

## Experiment setup

Code is written in Python, using SQLAlchemy. To also obtain execution plan and time we run the query twice, once using EXPLAIN ANALYZE, and once without.

The application is run three times, and makes the following actions:

Shared actions:
- Query zipcoderanges for all lat/long combinations within the target box with given radius (using EXPLAIN ANALYZE)
- Make the same query without EXPLAIN ANALYZE

Not indexed:
- Drop index if exists
- Perform shared actions

B-Tree index:
- Drop index if exists
- Create btree index on ZipcodeRange, based on the output of the `ll_to_earth(latitude, longitude)` function
- Perform shared actions

R-Tree index:
- Drop index if exists
- Create rtree (gist) index on ZipcodeRange, based on the output of the `ll_to_earth(latitude, longitude)` function
- Perform shared actions

Used python commands:

No index: `python -m rangefinder -d --closest --output notree.log`

B-Tree: `python -m rangefinder -i btree --closest --output btree.log`

R-Tree: `python -m rangefinder -i rtree --closest --output rtree.log`

## Experiment output

All queries returned the same result rows.

Not indexed: 
- Planning time: 4.350 ms
- Execution time: 13870.665 ms

B-Tree index:
- Planning time: 2.466 ms
- Execution time: 9747.789 ms

R-Tree index:
- Planning time: 4.273 ms
- Execution time: 0.425 ms

## Conclusions

Planning time remained mostly equal over indexes. The real difference was found in execution times.

As expected, R-Trees performed best, followed by B-Trees. Both indexes were faster than not using any.
B-Trees performed somewhat better than no index (1.4 times as fast), but nowhere near as well as R-Trees. The R-Tree reduced the execution time by orders of magnitude: from tens to tenths of seconds.