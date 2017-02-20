from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName("Descriptors of a Bad Business")
sc = SparkContext(conf=conf)

reviews = sc.textFile("hdfs:///shared/yelp/yelp_academic_dataset_review.json")

with open('descriptors_of_bad_business.txt', 'w+') as f:
    pass
