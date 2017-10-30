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

