from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, window, avg
from pyspark.sql.types import StructType, StructField, FloatType
import os
from pyspark.sql.types import StringType

spark = SparkSession.builder \
    .appName("KafkaSparkStreamingMovingAverage") \
    .getOrCreate()

# Assuming your Kafka setup and topic name are correctly configured
KAFKA_BROKER_SERVER = os.environ['KAFKA_BROKER_SERVER']
TOPIC_NAME = "stock_data"

# Define the schema of the Kafka data (if it's just a float value, adjust as necessary)
schema = StructType([
      StructField("stock_symbol", StringType(), True),
      StructField("price", FloatType(), True)
    ])

# Subscribe to the topic
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", KAFKA_BROKER_SERVER) \
  .option("subscribe", TOPIC_NAME) \
  .load()

# Deserialize the Kafka data
deserialized_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("parsed_value")) \
    .select("parsed_value.*")


# Start the streaming query
query = deserialized_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()