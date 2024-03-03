from kafka_producer import Data_source
from Spark_Processing.spark-processor import SparkProcessor

import os
import time

    publish = os.getenv('PUBLISH')

data_source = Data_source("sink") # creates a new sink topic

while True:
    data = SparkProcessor("stock_data") # fetch financial data
    data_source.start_stream_data(data) # need to pass in json data
    time.sleep(1)





