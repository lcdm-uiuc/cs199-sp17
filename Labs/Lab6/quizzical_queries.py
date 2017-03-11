import csv
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
conf = SparkConf().setAppName("Quizzical Queries")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
schema = "Id,ProductId,UserId,ProfileName,HelpfulnessNumerator,HelpfulnessDenominator,Score,Time,Summary,Text".split(',')


def parse_csv(x):
    x = x.replace('\n', '')
    d = csv.reader([x])
    return next(d)

reviews = sc.textFile("hdfs:///shared/amazon_food_reviews.csv")
first = reviews.first()
csv_payloads = reviews.filter(lambda x: x != first).map(parse_csv)

# Do your queries here

with open('quizzical_queries.txt', 'w+') as f:
    pass
