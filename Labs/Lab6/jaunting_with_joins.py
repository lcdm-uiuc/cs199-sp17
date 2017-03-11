from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
conf = SparkConf().setAppName("Jaunting With Joins")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

reviews = sqlContext.jsonFile("hdfs:///shared/yelp/yelp_academic_dataset_review.json")
businesses = sqlContext.jsonFile("hdfs:///shared/yelp/yelp_academic_dataset_business.json")
checkins = sqlContext.jsonFile("hdfs:///shared/yelp/yelp_academic_dataset_checkin.json")
users = sqlContext.jsonFile("hdfs:///shared/yelp/yelp_academic_dataset_user.json")

sqlContext.registerDataFrameAsTable(reviews, "reviews")
sqlContext.registerDataFrameAsTable(businesses, "businesses")
sqlContext.registerDataFrameAsTable(checkins, "checkins")
sqlContext.registerDataFrameAsTable(users, "users")

# Do your queries here

with open('jaunting_with_joins.txt', 'w+') as f:
    pass
