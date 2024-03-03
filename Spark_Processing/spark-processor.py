from pyspark.sql import SparkSession
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

import os

class SparkProcessor:
    def __init__(self,topic_name="stock_data"):
        self.spark = SparkSession.builder \
            .appName("KafkaSparkStreaming") \
            .getOrCreate()

        self.TOPIC_NAME = topic_name
        self.KAFKA_BROKER_SERVER = os.environ['KAFKA_BROKER_SERVER']

    def data_processing(self, data, type):
        """
        Data processing pipeline
        @param
        data: data (Json) to process 
        """
        if type == "self_compile":
            data = data.map(labda x: x+1)
        
        elif type =="": 
            pass
        
        
        return self.state_management(data)
    
    def state_management(self, data):
        """
        State management for the data

        @param
        data: data (Json) to process
        """
        return self.windowing(data)
    
    def windowing(self, data):
        """
        Windowing for the data

        @param
        data: data (Json) to process
        """
        return self.sink(data)

    def sink(self, data):
        """
        Sink for the data

        @param
        data: data (Json) to process
        """
        
        type_info=Types.ROW([Types.INT(), Types.STRING()]).build()
        kafka_producer = FlinkKafkaProducer(
        topic='test_sink_topic',
        serialization_schema=serialization_schema, # 
        producer_config={'bootstrap.servers': 'localhost:9093', 'group.id': 'test_group'})
        ds.add_sink(kafka_producer)

        return data
    
    def getjsonschema(self):
        return StructType([
            StructField("stock_symbol", StringType(), True),
            StructField("price", StringType(), True),
            StructField("time_stamp", StringType(), True)
        ])

                
    def process(self):

        # Subscribe to 1 topic
        df = self.spark \
          .readStream \
          .format("kafka") \
          .option("kafka.bootstrap.servers", self.KAFKA_BROKER_SERVER) \
          .option("subscribe", self.TOPIC_NAME) \
          .load()
        
        # Define the schema for the data
        schema = self.getjsonschema()
        
        parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("parsed_value"))
        
        
        # pass the data into the pipeline
        data = self.data_processing(parsed_df,'financial')
        return data

    if __name__ == "__main__":
        Processor = SparkProcessor()
        Processor.process()