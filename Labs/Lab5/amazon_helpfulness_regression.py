from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName("Amazon Helpfulness Regression")
sc = SparkContext(conf=conf)

reviews = sc.textFile("hdfs:///shared/amazon_food_reviews.csv")

with open('amazon_helpfulness_regression.txt', 'w+') as f:
    pass
