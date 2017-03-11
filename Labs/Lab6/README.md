# Lab 6: Spark SQL

## Introduction

Spark SQL is a powerful way for interacting with large amounts of structured data. Spark SQL gives us the concept of "dataframes", which will be familiar if you've ever done work with Pandas or R. DataFrames can also be thought of as similar to tables in databases.

With Spark SQL Dataframes we can interact with our data using the Structured Query Language (SQL). This gives us a declarative way to query our data, as opposed to the imperative methods we've studied in past weeks (i.e. discrete operations on sets of RDDs)

## SQL Crash Course

SQL is a declarative language used for querying data. The simplest SQL query is a `SELECT - FROM - WHERE` query. This selects a set of attributes (SELECT) from a specific table (FROM) where a given set of conditions holds (WHERE).

However, SQL also has a series of more advanced aggregation commands for grouping data. This is accomplished with the `GROUP BY` keyword. We can also join tables on attributes or conditions with the set of `JOIN ... ON` commands. We won't be expecting advanced knowledge of these more difficult topics, but developing a working understanding of how these work will be useful in completing this lab.

Spark SQL has a pretty good [Programming Guide](https://spark.apache.org/docs/1.5.1/sql-programming-guide.html) that's worth looking at.

Additionally, you may find [SQL tutorials](https://www.w3schools.com/sql/default.asp) online useful for this assignment.

## Examples

### Loading Tables

The easiest way to get data into Spark SQL is by registering a DataFrame as a table. A DataFrame is essentially an instance of a Table: it has a schema (columns with data types and names), and data.

We can create a DataFrame by passing an RDD of data tuples and a schema to `sqlContext.createDataFrame`:

```
data = sc.parallelize([('Tyler', 1), ('Quinn', 2), ('Ben', 3)])
df = sqlContext.createDataFrame(data, ['name', 'instructor_id'])
```

This creates a DataFrame with 2 columns: `name` and `instructor_id`.

We can then register this frame with the sqlContext to be able to query it generally:

```
sqlContext.registerDataFrameAsTable(df, "instructors")
```

Now we can query the table:

```
sqlContext.sql("SELECT name FROM instructors WHERE instructor_id=3")
```

### Specific Business Subset

Suppose we want to find all the businesses located in Champaign, IL that have 5 star ratings. We can do this with a simple `SELECT - FROM - WHERE` query:

```python
sqlContext.sql("SELECT * "
               "FROM businesses "
               "WHERE stars=5 "
               "AND city='Champaign' AND state='IL'").collect()
```

This selects all the rows from the `businesses` table that match the criteria described in the `WHERE` clause.

### Highest Number of Reviews

Suppose we want to rank users by how many reviews they've written. We can do this query with aggregation and grouping:

```python
sqlContext.sql("SELECT user_id, COUNT(*) AS c"
               "FROM reviews "
               "GROUP BY user_id "
               "SORT BY c DESC "
               "LIMIT 10").collect()
```

This query groups rows by the `user_id` column, and collapses those rows into tuples of `(user_id, COUNT(*))`, where `COUNT(*)` is the number of collapsed rows per grouping. This gives us the review count of each user. We then do `SORT BY c DESC` to show the top counts first, and `LIMIT 10` to only show the top 10 results.

## Lab Activities
**Lab 6 is due on Thursday, March 16th, 2017 at 11:55PM.**

Please zip your source files **and your output text files** for the following exercises and upload it to Moodle (learn.illinois.edu).

**NOTE:**

* For each of these problems you may use RDDs *only* for loading in and saving data to/from HDFS. All of your "computation" must be performed on DataFrames, either via the SQLContext or DataFrame interfaces.
* We _suggest_ using the SQLContext for most of these problems, as it's generally a more straight-forward interface.

### 1. Quizzical Queries

For this problem, we'll construct some simple SQL queries on the Amazon Review dataset that we used last week. Your first task is to create a DataFrame from the CSV set. Once you've done this, write queries that get the requested information about the data. Format and save your output and include it in your submission.

**NOTE:** For this problem, you *must* use `sqlContext.sql` to run your queries. This means, you have to run `sqlContext.registerDataFrameAsTable` on your constructed DataFrame and write queries in raw SQL.

Queries:

1. What is the review text of the review with id `22010`?
2. How many 5-star ratings does product `B000E5C1YE` have?
3. How any unique users have written reviews?

Notes:

* You'll want to use `csv.reader` to parse your data. Using `str.split(',')` is insufficient, as there will be commas in the Text field of the review.

### 2. Aggregation Aggravation

For this problem, we'll use some more complicated parts of the SQL language. Often times, we'll want to learn aggregate statistics about our data. We'll use `GROUP BY` and aggregation methods like `COUNT`, `MAX`, `AVG` to find out more interesting information about our dataset.

Queries:

1. How many reviews has the person who has written the most number of reviews written? What is that user's UserId?
2. List the ProductIds of the products with the top 10 highest average review scores of products that have more than 10 reviews, sorted by product score, with ties broken by number of reviews.
3. List the Id of the reviews with the top 10 highest ratios between `HelpfulnessNumerator` and `HelpfulnessDenominator`, which have `HelpfulnessDenominator` more than 10, sorted by that ratio, with ties broken by `HelpfulnessDenominator`.

Notes: 

* You'll want to use `csv.reader` to parse your data. Using `str.split(',')` is insufficient, as there will be commas in the Text field of the review.
* You may use DataFrame query methods other than `sqlContext.sql`, but you must still do all your computations on DataFrames.

### 3. Jaunting with Joins

For this problem, we'll switch back to the Yelp dataset. Note that you can use the very handy [jsonFile](https://spark.apache.org/docs/1.5.1/api/python/pyspark.sql.html#pyspark.sql.SQLContext.jsonFile) method to load in the dataset as a DataFrame.

There are some times that we need to access data that is split accross multiple tables. For instance, when we look at a single Yelp review, we cannot directly get the user's name, because we only have their id. But, we can match users with their reviews by "joining" on their user id. The database does this by looking for rows with matching values for the join columns.

You'll want to look up the JOIN (specifically INNER JOIN) SQL commands for these problems.

Queries:
1) What state has had the most Yelp check-ins?
2) What is the maximum number of "funny" ratings left on a review created by someone who's been yelping since 2012?
3) List the user ids of anyone who has left a 1-star review, has created more than 250 reviews, and has left a review in Champaign, IL.

Notes: 

* You may use DataFrame query methods other than `sqlContext.sql`, but you must still do all your computations on DataFrames.