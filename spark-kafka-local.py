import sys
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.streaming.kafka import TopicAndPartition
import requests
from operator import add
from nltk.corpus import stopwords


def sendTopWords(counts, url):
    def takeAndSend(time, rdd):
        if not rdd.isEmpty():
            word_counts = rdd.take(10)

            words = []
            values = []

            for (word, count) in word_counts:
                words.append(word)
                values.append(count)

            json_data = {'words': str(words), 'counts': str(values)}
            print(json_data)

            response = requests.post(url, data=json_data)

    counts.foreachRDD(takeAndSend)


def sendTweets(tweets, url):
    def takeAndSend(time, rdd):
        if not rdd.isEmpty():
            tweets_data = rdd.take(2)

            users = []
            texts = []

            for (user, text) in tweets_data:
                users.append(user)
                texts.append(text)

            json_data = {'user': str(users), 'text': str(texts)}
            print(json_data)

            response = requests.post(url, data=json_data)

    tweets.foreachRDD(takeAndSend)
    
def sendTopWords(counts, url):
    def takeAndSend(time, rdd):
        if not rdd.isEmpty():
            word_counts = rdd.take(10)

            words = []
            values = []

            for (word, count) in word_counts:
                words.append(word)
                values.append(count)

            json_data = {'words': str(words), 'counts': str(values)}
            print(json_data)

            response = requests.post(url, data=json_data)

    counts.foreachRDD(takeAndSend)


def sendTweetsFromStream(kvs, url):
    tweets = kvs.map(lambda x: x[1].encode("ascii", "ignore")) \
                .map(lambda x: json.loads(x)) \
                .map(lambda json_object: (json_object["user"]["screen_name"], json_object["text"]))
    sendTweets(tweets, server + 'update_tweets')

def sendTopWordsFromStream(kvs, url):
    tweets = kvs.map(lambda x: x[1].encode("ascii", "ignore")) \
                .map(lambda x: json.loads(x)) \
                .map(lambda json_object: (json_object["user"]["screen_name"], json_object["text"]))

    lines = tweets.flatMap(lambda line: line[1].split(" "))

    ## This part does the hashtag count
    hashtag_counts = lines.filter(lambda word: len(word) >= 2 and word[0] == '#') \
                          .map(lambda word: (word, 1)) \
                          .reduceByKey(add) \
                          .transform(lambda rdd: rdd.sortBy(lambda x: x[1], ascending = False))
    hashtag_counts.pprint()
    sendTopWords(hashtag_counts, server + 'update_counts')

    return False


if __name__ == "__main__":
    sc = SparkContext(appName = "TwitterDataAnalysis")
    sc.setLogLevel("ERROR")

    ssc = StreamingContext(sc, 10)
    brokers, topic = sys.argv[1:]
    
    #partition = 0
    #start = 1
    #topicpartition = TopicAndPartition(topic, partition)
    #fromoffset = {topicpartition: 0}
    #fromOffsets = {TopicAndPartition(topic, partition): int(start)}

    kvs = KafkaUtils. \
        createDirectStream(ssc, [topic], {"metadata.broker.list": brokers, "auto.offset.reset": "smallest"})
    #kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers}, fromOffsets)

    tweets = kvs.map(lambda x: x[1].encode("ascii", "ignore")) \
                .map(lambda x: json.loads(x)) \
                .map(lambda json_object: (json_object["user"]["screen_name"], json_object["text"]))
    tweets.pprint()

    
    '''
    ## This part filters the tweets
    filtered_tweets = tweets.filter(lambda kv: filter_layoffs(kv[1]))
    filtered_tweets.pprint()
    '''

    lines = tweets.flatMap(lambda line: line[1].split(" "))

    ## This part does the hashtag count
    hashtag_counts = lines.filter(lambda word: len(word) >= 2 and word[0] == '#') \
                          .map(lambda word: (word, 1)) \
                          .reduceByKey(add) \
                          .transform(lambda rdd: rdd.sortBy(lambda x: x[1], ascending = False))
    hashtag_counts.pprint()

    '''
    ## This part does the word count
    sw = stopwords.words('english')
    sw.extend(['rt', 'https', 'http', 'coronavirus', 'covid19', 'covid-19'])

    counts = lines.map(lambda word: word.strip().lower()) \
                  .filter(lambda word: word not in sw) \
                  .filter(lambda word: len(word) >= 2 and word[0] != '#' and word[0] != '@') \
                  .map(lambda word: (word, 1)) \
                  .reduceByKey(add) \
                  .transform(lambda rdd: rdd.sortBy(lambda x: x[1], ascending = False))
    counts.pprint()
    '''

    server = 'http://localhost:5000/'
    #sendTweets(tweets, server + 'update_tweets')
    #sendTopWords(hashtag_counts, server + 'update_counts')
    sendTweetsFromStream(kvs, server + 'update_tweets')
    sendTopWordsFromStream(kvs, server + 'update_counts')

    ssc.start()
    ssc.awaitTerminationOrTimeout(60)
    ssc.stop(stopGraceFully = True)
