from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os

spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .getOrCreate()

# We will keep the consumer running for 10 seconds
KAFKA_BROKER_SERVER = os.environ['KAFKA_BROKER_SERVER']
TOPIC_NAME = "stock_data"

# Subscribe to 1 topic
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", KAFKA_BROKER_SERVER) \
  .option("subscribe", TOPIC_NAME) \
  .load()


# Correctly cast the value from Kafka as a Float
deserialized_df = df.selectExpr("CAST(value AS STRING) as value").selectExpr("CAST(value AS FLOAT) as floatValue") # this is the main data frame that we want to process

# Simplify the output to show just the value column
query = deserialized_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()