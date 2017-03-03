from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName("Amazon Review Classification")
sc = SparkContext(conf=conf)

reviews = sc.textFile("hdfs:///shared/amazon_food_reviews.csv")

with open('amazon_review_classification.txt', 'w+') as f:
    pass
