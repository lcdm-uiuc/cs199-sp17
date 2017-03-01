# Lab 4: Spark

## Introduction

As we have talked about in lecture, Spark is built on what's called a Resilient Distributed Dataset (RDD). 

PySpark allows us to interface with these RDD’s in Python. Think of it as an API. In fact, it is an API; it even has its own [documentation](http://spark.apache.org/docs/latest/api/python/)! It’s built on top of the Spark’s Java API and exposes the Spark programming model to Python.


PySpark makes use of a library called `Py4J`, which enables Python programs to dynamically access Java objects in a Java Virtual Machine.

This allows data to be processed in Python and cached in the JVM.


## Running your Jobs

We'll be using `spark-submit` to run our spark jobs on the cluster. `spark-submit` has a couple command line options that you can tweak.

#### `--master`
This option tells `spark-submit` where to run your job, as spark can run in several modes.

* `local`
    * The spark job runs locally, without using any compute resources from the cluster.
* `yarn-client`
    * The spark job runs on our YARN cluster, but the driver is local to the machine, so it 'appears' that you're running the job locally, but you still get the compute resources from the cluster. You'll see the logs spark provides as the program executes.
    * When the cluster is busy, you *will not* be able to use this mode, because it imposes too much of a memory footprint.
* `yarn-cluster`
    * The spark job runs on our YARN cluster, and the spark driver is in some arbitrary location on the cluster. This option doesn't give you logs directly, so you'll have to get the logs manually.
    * In the output of `spark-submit --master yarn-cluster` you'll find an `applicationId`. (This is similar to when you ran jobs on Hadoop). You can issue this command to get the logs for your job:

        ```
        yarn logs -applicationId <YOUR_APPLICATION_ID> | less
        ```
    * When debugging Python applications, it's useful to `grep` for `Traceback` in your logs, as this will likely be the actual debug information you're looking for.

        ```
        yarn logs -applicationId <YOUR_APPLICATION_ID> | grep -A 50 Traceback
        ```
        
    * *NOTE*: In cluster mode, normal IO operations like opening files will behave unexpectedly! This is because you're not guaranteed which node the driver will run on. You must use the PySpark API for saving files to get reliable results. You also have to coalesce your RDD into one partition before asking PySpark to write to a file (why do you think this is?). Additionally, you should save your results to HDFS.

        ```python
        <my_rdd>.coalesce(1).saveAsTextFile('hdfs:///user/MY_USERNAME/foo')
        ```

#### `--num-executors`
This option lets you set the number of executors that your job will have. A good rule of thumb is to have as many executors as the maximum number of partitions an RDD will have during a Spark job (this heuristic holds better for simple jobs, but falls apart as the complexity of your job increases).

The number of executors is a tradeoff. Too few, and you might not be taking full advantage of Sparks parallelism. However, there is also an upper bound on the number of executors (for obvious reasons), as they have a fairly large memory footprint. (Don't set this too high or we'll terminate your job.)

You can tweak executors more granularly by setting the amount of memory and number of cores they're allocated, but for our purposes the default values are sufficient.

### Putting it all together

Submitting a spark job will ususally look something like this:

```
spark-submit --master yarn-cluster --num-executors 10 MY_PYTHON_FILE.py
```

Be sure to include the `--master` flag, or else your code will only run locally, and you won't get the benefits of the cluster's parallelism.

### Interactive Shell

While `spark-submit` is the way we'll be endorsing to run PySpark jobs, there is an option to run jobs in an interactive shell. Use the `pyspark` command to load into the PySpark interactive shell. You can use many of the same options listed above to tweak `pyspark` settings, such as `--num-executors` and `--master`.

Note: If you start up the normal `python` interpreter, you probably won't be able to use any of the PySpark features.

### Helpful Hints

* You'll find the [PySpark documentation](https://spark.apache.org/docs/2.0.0/api/python/pyspark.html#pyspark.RDD) (especially the section on RDDs) very useful.
* Run your Spark jobs on a subset of the data when you're debugging. Even though Spark is very fast, jobs can still take a long time - especially when you're working with the review dataset. When you are experimenting, always use a subset of the data. The best way to use a subset of data is through the [take](https://spark.apache.org/docs/1.6.2/api/java/org/apache/spark/rdd/RDD.html#take(int)) command.
* [Programming Guide](http://spark.apache.org/docs/latest/programming-guide.html) -- This documentation by itself could be used to solve the entire lab. It is a great quickstart guide about Spark.


## The Dataset

This week, we'll be working off of a set of released Yelp data.

The dataset is located in `/shared/yelp` in HDFS. We'll be using the following files for this lab:

```
/shared/yelp/yelp_academic_dataset_business.json
/shared/yelp/yelp_academic_dataset_checkin.json
/shared/yelp/yelp_academic_dataset_review.json
/shared/yelp/yelp_academic_dataset_user.json
```

We'll give more details about the data in these files as we continue with the lab, but the general schema is this: each line in each of these JSON files is an independently parsable JSON object that represents a distinct entity, whether it be a business, a review, or a user.

*Hint:* JSON is parsed with `json.loads`

## Lab Activities
**Lab 4 is due on Thursday, March 2nd, 2017 at 11:55PM.**

Please zip your source files **and your output text files** for the following exercises and upload it to Moodle (learn.illinois.edu).

### 1. Least Expensive Cities

In planning your next road trip, you want to find the cities that, overall, will be the least expensive to dine at.

It turns out that Yelp keeps track of a handy metric for this, and many restaurants have the attribute `RestaurantsPriceRange2` that gives the business a score from 1-4 as far as 'priciness'.

Write a PySpark application that sorts cities by the average price of their businesses/restaurants.

Notes:

* Discard any business that does not have the `RestaurantsPriceRange2` attribute
* Discard any business that does not have a valid city and state
* Your output should be sorted descending by average price (highest at top, lowest at bottom). Your average restaurant price should be rounded to 2 decimal places. Each city should get a row in the output and look like:

	`CITY, STATE: PRICE`

### 2. Up All Night

You also expect on this road trip that you'll be out pretty late. Yelp also lists the hours that businesses are open, so lets find out where you'll be likely to find something to eat late at night.

Write a PySpark application that sorts cities by the median closing time of their businesses/restaurants to find the cities that are open latest.

Notes:

* Discard any business that doesn't have a valid `hours` property, or an `hours` property that does not include the closing time of the business
* Discard any invalid times (some business have `DAY 0:0-0:0` as their hours, which we consider to be invalid), and for simplicities sake, assume that all businesses close before midnight.
* Use the **median** closing time of businesses in each city as the "city closing time". If you have to tie break (i.e. `num_business_hours % 2 == 1`), choose the lower of the two so you can avoid doing datetime math
* Your output should be in the following format, with median closing time in `HH:MM` (24 hour clock) format and should be sorted descending by time (latest cities first).
	
	`CITY, STATE: HH:MM`

### 3. Pessimistic Yelp Reviewers

For this activity, we'll be looking at [Yelp reviews](https://www.youtube.com/watch?v=QEdXhH97Z7E). 😱 Namely, we want to find out which Yelp reviewers are... more harsh than they should be.

To do this we will calculate the average review score of each business in our dataset, and find the users that most often under-rate businesses.

Use the following to calculate which users are pessimistic:

* The `average_business_rating` of a business is the sum of the ratings of the business divided by the count of the ratings for that business.
* A user's pessimism score is the sum of the differences between their rating and the average business rating *if and only if* their rating is lower than the average divided by the number of times their rating was less than the average.

Your output should contain the top 100 pessimistic users in the following format, where `pessimism_score` is rounded to 2 decimal places, and users are sorted in descending order by `pessimism_score`:

```
user_id: pessimism_score
```

Notes:

* Business have "average rating" as a property. We **will not** be using this. Instead - to have greater precision - we will be manually calculating a business' average reviews by averaging all the review scores given in `yelp_academic_dataset_review.json`.
* Discard any reviews that do not have a rating, a `user_id`, and a `business_id`.

### 4. Descriptors of a Bad Business

Suppose we want to predict a review's score from its text. There are many ways we could do this, but a simple way would be to find words that are indicative of either a positive or negative review.

In this activity, we want to find the words that are the most 'charged'. We can think about the probability that a word shows up in a review as depending on the type of a review. For example, it is more likely that "delicious" would show up in a positive review than a negative one.

Calculate the probability of each word appearing to be the number of occurrences of the word in the category tested (positive/negative) divided by the number of reviews in that category.

Output the **top 250** words that are most likely to be in negative reviews, but not in positive reviews (maximize `P(negative) - P(positive)`).

Notes:

* Remove any words listed in `nltk`'s list of [English stopwords](http://www.nltk.org/book/ch02.html#wordlist-corpora) and remove all punctuation. We also encourage you to use `nltk.tokenize.word_tokenize` to split reviews into words.
* Consider a review to be positive if it has >=3 stars, and consider a review negative if it has <3 stars.
* Your output should be as follows, where `probability_diff` is `P(negative) - P(positive)` rounded to **5** decimal places and sorted in descending order:

	`word: probability_diff`
