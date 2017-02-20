from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName("Pessimistic Users")
sc = SparkContext(conf=conf)

reviews = sc.textFile("hdfs:///shared/yelp/yelp_academic_dataset_review.json")

with open('pessimistic_users.txt', 'w+') as f:
    f.write('taeyoung_kim: 1.23')
