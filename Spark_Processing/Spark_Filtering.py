from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, window, avg
from pyspark.sql.types import StructType, StructField, FloatType
import os

spark = SparkSession.builder \
    .appName("KafkaSparkStreamingMovingAverage") \
    .getOrCreate()

# Assuming your Kafka setup and topic name are correctly configured
KAFKA_BROKER_SERVER = os.environ['KAFKA_BROKER_SERVER']
TOPIC_NAME = "stock_data"

# Define the schema of the Kafka data (if it's just a float value, adjust as necessary)
schema = StructType([StructField("value", FloatType())])

# Subscribe to the topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER_SERVER) \
    .option("subscribe", TOPIC_NAME) \
    .load()

# Deserialize the data assuming it's JSON, adjust according to your actual data format
deserialized_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Calculate moving average over a specified window
# Adjust the window duration and slide duration as needed
movingAvg = deserialized_df \
    .groupBy(window(col("timestamp"), "1 minute", "30 seconds")) \
    .agg(avg("value").alias("movingAverage"))

# Convert to a Python dictionary and print. Note: This is a simplification for illustration.
# In practice, you might need to adjust this to properly serialize and output your data.
query = movingAvg \
    .writeStream \
    .outputMode("update") \
    .foreachBatch(lambda df, epoch_id: df.collect().foreach(print)) \
    .start()

query.awaitTermination()
