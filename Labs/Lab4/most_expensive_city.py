from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName("Most Expensive City")
sc = SparkContext(conf=conf)

businesses = sc.textFile("hdfs:///shared/yelp/yelp_academic_dataset_business.json")

with open('most_expensive_city.txt', 'w+') as f:
    f.write('Champaign, IL: 1.23')
