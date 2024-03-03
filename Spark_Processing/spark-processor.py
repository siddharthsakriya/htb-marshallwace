from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os

class SparkProcessor:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("KafkaSparkStreaming") \
            .getOrCreate()

        self.TOPIC_NAME = "stock_data"
        self.KAFKA_BROKER_SERVER = os.environ['KAFKA_BROKER_SERVER']

    def process(self):

        # Subscribe to 1 topic
        df = self.spark \
          .readStream \
          .format("kafka") \
          .option("kafka.bootstrap.servers", self.KAFKA_BROKER_SERVER) \
          .option("subscribe", self.TOPIC_NAME) \
          .load()


        # Correctly cast the value from Kafka as a Float
        deserialized_df = df.selectExpr("CAST(value AS STRING) as value").selectExpr("CAST(value AS FLOAT) as floatValue")

        # Simplify the output to show just the value column
        query = deserialized_df \
            .writeStream \
            .outputMode("append") \
            .format("console") \
            .option("truncate", False) \
            .start()

        query.awaitTermination()