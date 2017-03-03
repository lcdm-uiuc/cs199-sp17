from pyspark.mllib.feature import HashingTF, IDF
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes
from pyspark.mllib.evaluation import MulticlassMetrics
import json
import nltk
from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName("Bayes Binary TFIDF")
sc = SparkContext(conf=conf)


def get_labeled_review(x):
    return x.get('stars'), x.get('text')


def categorize_review(x):
    return (0 if x[0] > 2.5 else 1), x[1]


def format_prediction(x):
    return "actual: {0}, predicted: {1}".format(x[0], float(x[1]))


def produce_tfidf(x):
    tf = HashingTF().transform(x)
    idf = IDF(minDocFreq=5).fit(tf)
    tfidf = idf.transform(tf)
    return tfidf

# Load in reviews
reviews = sc.textFile("hdfs:///shared/yelp/yelp_academic_dataset_review.json")
# Parse to json
json_payloads = reviews.map(json.loads)
# Tokenize and weed out bad data
labeled_data = (json_payloads.map(get_labeled_review)
                             .filter(lambda x: x[0] and x[1])
                             .map(lambda x: (float(x[0]), x[1]))
                             .map(categorize_review)
                             .mapValues(nltk.word_tokenize))
labels = labeled_data.map(lambda x: x[0])

tf = HashingTF().transform(labeled_data.map(lambda x: x[1]))
idf = IDF(minDocFreq=5).fit(tf)
tfidf = idf.transform(tf)
zipped_data = (labels.zip(tfidf)
                     .map(lambda x: LabeledPoint(x[0], x[1]))
                     .cache())

# Do a random split so we can test our model on non-trained data
training, test = zipped_data.randomSplit([0.7, 0.3])

# Train our model
model = NaiveBayes.train(training)

# Use our model to predict
train_preds = (training.map(lambda x: x.label)
                       .zip(model.predict(training.map(lambda x: x.features))))
test_preds = (test.map(lambda x: x.label)
                  .zip(model.predict(test.map(lambda x: x.features))))

# Ask PySpark for some metrics on how our model predictions performed
trained_metrics = MulticlassMetrics(train_preds.map(lambda x: (x[0], float(x[1]))))
test_metrics = MulticlassMetrics(test_preds.map(lambda x: (x[0], float(x[1]))))

with open('output_binary.txt', 'w+') as f:
    f.write(str(trained_metrics.confusionMatrix().toArray()) + '\n')
    f.write(str(trained_metrics.precision()) + '\n')
    f.write(str(test_metrics.confusionMatrix().toArray()) + '\n')
    f.write(str(test_metrics.precision()) + '\n')
