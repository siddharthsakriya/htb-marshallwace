# from pyspark.sql import SparkSession
# from datetime import datetime, timedelta
# import time
# import os

# # We will keep the consumer running for 10 seconds
# stop_time = datetime.now() + timedelta(seconds=10)  # 10 seconds from now
# KAFKA_BROKER_SERVER = os.environ['KAFKA_BROKER_SERVER']
# TOPIC_NAME = "stock_data"

# ##
# ## TODO TO UPDATE kafka.sasl.jaas.config
# ##
# kafka_options = {
#     "kafka.bootstrap.servers": KAFKA_BROKER_SERVER,
#     # "kafka.sasl.mechanism": "SCRAM-SHA-256",
#     # "kafka.security.protocol": "SASL_SSL",
#     # "kafka.sasl.jaas.config": """org.apache.kafka.common.security.scram.ScramLoginModule required username="XXX" password="YYY";""",
#     "startingOffsets": "earliest", # Start from the beginning when we consume from kafka
#     "subscribe": "stock"           # Our topic name
# }

# spark = SparkSession.builder \
#     .appName("KafkaSparkStreaming") \
#     .getOrCreate()

# # Subscribe to Kafka topic "hello"
# df = spark.readStream.format("kafka").options(**kafka_options).load()

# # Deserialize the value from Kafka as a String for now
# deserialized_df = df.selectExpr("CAST(value AS STRING)")

# # Query Kafka and wait 10sec before stopping pyspark
# query = deserialized_df.writeStream.outputMode("append").format("console").start()
# time.sleep(10)
# query.stop()

from pyspark.sql import SparkSession
from datetime import datetime, timedelta
import time
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

# # Deserialize the value from Kafka as a String for now
deserialized_df = df.selectExpr("CAST(value AS STRING)")

# # Query Kafka and wait 10sec before stopping pyspark
query = deserialized_df.writeStream.outputMode("append").format("console").start()


query.awaitTermination()