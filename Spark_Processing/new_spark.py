from pyspark.streaming.kafka import KafkaUtils
import os

KAFKA_BROKER_SERVER = os.environ['KAFKA_BROKER_SERVER']
TOPIC_NAME = "stock_data"

directKafkaStream = KafkaUtils.createDirectStream(ssc, [topic], {"bootstrap.servers": KAFKA_BROKER_SERVER})


offsetRanges = []

def storeOffsetRanges(rdd):
     global offsetRanges
     offsetRanges = rdd.offsetRanges()
     return rdd

def printOffsetRanges(rdd):
     for o in offsetRanges:
         print ("%s %s %s %s" % (o.topic, o.partition, o.fromOffset, o.untilOffset))

directKafkaStream\
     .transform(storeOffsetRanges)\
     .foreachRDD(printOffsetRanges)