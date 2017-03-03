from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName("Yelp Clustering")
sc = SparkContext(conf=conf)

businesses = sc.textFile("hdfs:///shared/yelp/yelp_academic_dataset_business.json")

with open('yelp_clustering.txt', 'w+') as f:
    pass