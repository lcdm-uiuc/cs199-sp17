from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName("Up All Night")
sc = SparkContext(conf=conf)

businesses = sc.textFile("hdfs:///shared/yelp/yelp_academic_dataset_business.json")

with open('up_all_night.txt', 'w+') as f:
    f.write('Champaign, IL: 11:59')
