# Lab 5: Spark MLlib

## Introduction

This week we'll be diving into another aspect of PySpark: MLlib. Spark MLlib provides an API to run machine learning algorithms on RDDs so that we can do ML on the cluster with the benefit of parallelism / distributed computing.

## Machine Learning Crash Course

We'll be considering 3 types of machine learning in the lab this week:

* Classification
* Regression
* Clustering

However, for most of the algoritms / feature extractors that MLlib provides, there is a common pattern:

1) Fit - Trains the model, using training data to adjust the model's internal parameters.

2) Transform - Use the fitted model to predict the label/value of novel data (data not used in the traning of the model).

If you go on to do more data science work, you'll see that this 2-phase ML pattern is common in other ML libraries, like `scikit-learn`.

Things are a bit more complicated in PySpark, because part of the way RDDs are handled (i.e. lazy evaluation), we often have to explicitly note when we want to predict data, and other instances when we're piping data through different steps of our model's setup.

It'll be extremely valuable to look up PySpark's documentation and example when working on this week's lab. The lab examples we'll be giving you do not require deep knowledge of Machine Learning concepts to complete. However, you will need to be good documentation-readers to naviaget MLlib's nuances.

## Examples

### TF-IDF Naive Bayes Yelp Review Classification

#### Extracting Features

Remember last week when you found out which words were corrolated with negative reviews by calculating the probability of a word occuring in a review? PySpark lets you do something like this extremely easily to calculate the Term Frequency - Inverse Document Frequency ([tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)) characteristics of a set of texts.

Let's define some terms:

* Term frequency - The number of times a word appears in a text
* Inverse document frequency - Weights a word's importance in a text by seeing if that word is rare in the collection of all texts. So, if we have a sentence contains the only reference to "cats" in an entire book, that sentence will have "cats" ranked as highly relevant.

TF-IDF combines the previous two concepts. Suppose we had a few sentences that refer to "cats" in a large book. We'd rank those rare sentences then by the frequency of the "cats" in each of those sentences.

There's a fair amount of math behind calculating TF-IDF, but for this lab it is sufficient to know that it is a relatively reliable way of guessing the relevance of a word in the context of a large body of data.

You'll also note that we're making use of a `HashingTF`. This is just a really quick way to compute the term-frequency of words. It uses a hash function to represent a long string with a shorter hash, and can use a datastructure like a hashmap to quickly count the frequency with which words appear.

#### Classifying Features

We'll also be using a [Naive Bayes](https://en.wikipedia.org/wiki/Naive_Bayes_classifier) classifier. This type of classifier looks at a set of data and labels, and constructs a model to preduct the label given the data using probabilistic means.

Again, it's not necessary to know the inner workings of Naive Bayes, just that we'll be using it to classify data.

#### Constructing a model

To construct a model, we'll need to construct an RDD that has (key, value) pairs with keys as our labels, and values as our features. First, however, we'll need to extract those features from the text. We're going to use TF-IDF as our feature, so we'll calculate that for all of our text first.

We'll start with the assumption that you've transformed the data so that we have `(label, array_of_words)` as the RDD. To start with, we'll have label be `0` if the review is negative and `1` if the review is positive. You practiced how to do this last week.

Here's how we'll extract the TF-IDF features:

```python
# Feed HashingTF just the array of words
tf = HashingTF().transform(labeled_data.map(lambda x: x[1]))

# Pipe term frequencies into the IDF
idf = IDF(minDocFreq=5).fit(tf)

# Transform the IDF into a TF-IDF
tfidf = idf.transform(tf)

# Reassemble the data into (label, feature) K,V pairs
zipped_data = (labels.zip(tfidf)
                     .map(lambda x: LabeledPoint(x[0], x[1]))
                     .cache())
```

Now that we have our labels and our features in one RDD, we can train our model:

```
# Do a random split so we can test our model on non-trained data
training, test = zipped_data.randomSplit([0.7, 0.3])

# Train our model with the training data
model = NaiveBayes.train(training)
```

Then, we can use this model to predict new data:
```python
# Use the test data and get predicted labels from our model
test_preds = (test.map(lambda x: x.label)
                  .zip(model.predict(test.map(lambda x: x.features))))
```

If we look at this `test_preds` RDD, we'll see our text, and the label the model predicted.

However, if we want a more precise measurement of how our model faired, PySpark gives us `MulticlassMetrics`, which we can use to measure our model's performance.

```python
trained_metrics = MulticlassMetrics(train_preds.map(lambda x: (x[0], float(x[1]))))
test_metrics = MulticlassMetrics(test_preds.map(lambda x: (x[0], float(x[1]))))

print trained_metrics.confusionMatrix().toArray()
print trained_metrics.precision()

print test_metrics.confusionMatrix().toArray()
print test_metrics.precision()
```

#### Analyzing our Results
`MulticlassMetrics` let's us see the ["confusion matrix"](https://en.wikipedia.org/wiki/Confusion_matrix) of our model, which shows us how many times our model chose each label given the actual label of the data point.

The meaning of the columns is the _predicted_ value, and the meaning of the rows is the _actual_ value. So, we read that `confusion_matrix[0][1]` is the number of items predicted as having `label[1]` that were in actuality `label[0]`.

Thus, we want our confusion matrix to have as many items on the diagonals as possible, as these represent items that were correctly predicted.

We can also get precision, which is a more simple metric of "how many items we predicted correctly".

Here's our results for this example:

```
# Training Data Confusion Matrix:
[[ 2019245.   115503.]
 [  258646.   513539.]]
# Training Data Accuracy:
0.8712908071840665

# Testing Data Confusion Matrix:
[[ 861056.   55386.]
 [ 115276.  214499.]]
#Testing Data Accuracy:
0.8630559525347512
```

Not terrible. As you see, our training data get's slightly better prediction precision, because it's the data used to train the model.

#### Extending the Example

What if instead of just classifying on positive and negative, we try to classify reviews based on their 1-5 stars review score?

```
# Training Data Confusion Matrix:
[[ 130042.   38058.   55682.  115421.  193909.]
 [  27028.   71530.   26431.   55381.   95007.]
 [  35787.   22641.  102753.   71802.  122539.]
 [  72529.   45895.   69174.  254838.  246081.]
 [ 113008.   73249.  108349.  225783.  535850.]]
# Training Data Accuracy:
0.37645263439801124

# Testing Data Confusion Matrix:
[[  33706.   20317.   27553.   54344.   90325.]
 [  15384.   10373.   14875.   28413.   46173.]
 [  18958.   13288.   19389.   37813.   59746.]
 [  36921.   25382.   37791.   76008.  120251.]
 [  57014.   37817.   55372.  112851.  194319.]]
#Testing Data Accuracy:
0.268241369417615
```

Ouch. What went wrong? Well, a couple things. One thing that hurts us is that Naive Bayes is, well, Naive. While we intuitively know that the meanings 1, 2, 3, 4, 5 have a specific value, NB doesn't have any concept that items labeled 4 and 5 are probably going to be closer than a pair labeled 1 and 5.

Also, in this example we see a case where testing out training data doesn't have much utility. While an accuracy of `0.376` isn't great, it's still a lot better thatn `0.268`. Validating on the training data would lead us to think that our model is substantially more accurate than it actually is.

#### Conclusion

The full code of the first example is in `bayes_binary_tfidf.py`, and the second "extended" example is in `bayes_tfidf.py`.

## Lab Activities
**Lab 5 is due on Thursday, March 9th, 2017 at 11:55PM.**

Please zip your source files **and your output text files** for the following exercises and upload it to Moodle (learn.illinois.edu).

**NOTE:** 

* For each problem you may only use, at most, 80% of the dataset to train on. The other 20% should be used for testing your model. (i.e. use `rdd.randomSplit([0.8, 0.2]))
* Our cluster has PySpark version 1.5.2. This is a slightly older version, so we don't have a couple of the cutting-edge ML tools. Use [this](https://spark.apache.org/docs/1.5.0/api/python/pyspark.html#) documentation in your research.

#### Precision Competition

Lab Problems 1 and 2 have an aspect of competition this week: We'll be awarding 10% extra credit on this lab to the top 3 students with the highest average precision across the two problems. Make sure that your spark jobs outputs the precision of your models as given by the appropriate metrics class, and that your results are reproducable to be eligable for credit.

### 1. Amazon Review Score Classification
This week, we'll be using an Amazon dataset of food reviews. You can find this dataset in HDFS at `/shared/amazon_food_reviews.csv`. The dataset has the following columns:

```
Id, ProductId, UserId, ProfileName, HelpfulnessNumerator, HelpfulnessDenominator, Score, Time, Summary, Text
```
Similar to the Yelp Dataset, Amazon's food review dataset provides you with some review text and a review score. Use MLlib to classify these reviews by score. You can use any classifiers and feature extractors that are available. You may also choose to classify either on positive/negative or the more granular stars rating. You'll only be eligable for the precision contest if you classify on stars, not just positive/negative.

Notes:

* You can use the any fields other than `HelpfulnessNumerator` or `HelpfulnessDenominator` for feature extraction.
* Use `MulticlassMetrics` to output the `confusionMatrix` and `precision` of your model. You want to maximize the precision. Include this output in your submission.

### 2. Amazon Review Helpfulness Regression

Amazon also gives a metric of "helpfulness". The dataset has the number of users who marked a review as helpful, and the number of users who voted either up or down on the review.

Define a review's helpfulness score as `HelpfulnessNumerator / HelpfulnessDenominator`.

Construct and train a model that uses a regression algorithm to predict a review's helpfulnes score from it's text. 

Notes:

* You can use the any fields other than `Score` for feature extraction.
* We suggest that at for a starting point, you use `pyspark.mllib.regression.LinearRegressionWithSGD` as your regression model.
* Use `pyspark.mllib.evaluation.RegressionMetrics` to output the `explainedVariance` and `rootMeanSquaredError`. You want to minimize the error.

### 3. Yelp Business Clustering

Going back to the Yelp dataset, suppose we want to find clusters of business in the Urbana/Champaign area. Where do businesses aggregate geographically? Could we predict from a set of coordinates which cluster of business a given business is in? Use K-Means to come up with a clustering model for the U-C area.

How can we determine how good our model is? The simplest way is to just graph it, and see if the clusters match what we would expect. More formally, we can use Within Set Sum of Squared Error ([WSSSE](https://spark.apache.org/docs/1.5.0/mllib-clustering.html#k-means)) to determin the optimal number of clusters. If we plot the error for multiple values of k, we can see the point of diminishing returns to adding more clusters. You should pick a value of k that is around this point of diminishing return.

Notes:

* Use `pyspark.mllib.clustering.KMeans` as your clustering algorithm.
* Your task is to:
    1. Extract the business that are in the U-C area and use their coordinates as features for your KMeans clustering model.
    2. Select a proper K such that you get a good approximation of the "actual" clusters of businesses. (May require trial-and-error)
    3. Plot the businesses with `matplotlib.pyplot.scatter` and have each point on the scatter plot be color-keyed by their cluster.
    4. Include both the plot as a PNG and a short justification for your k value (either in comments in your code or in a separate `.txt`) in your submission.
