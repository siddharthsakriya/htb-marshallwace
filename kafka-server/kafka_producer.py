from kafka import KafkaProducer
import time
import os
import json

KAFKA_BROKER = os.environ['KAFKA_BROKER_SERVER']

class Data_source():
    """
    Initialise a new class for each new topic that you want to publish to
    """
    def __init__(self,topic_name=''):
        """Initialises stuff for Kafka
         @param
        topic_name: name of the topic to publish to"""

        self.latency = 0.01
        self.kafka_topic = topic_name
        self.bootstrap_servers = [KAFKA_BROKER]
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers,api_version=(0,11,5),value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    def start_stream_data(self, value):
        """Streams data to Kafka
        @param
        value: value to publish to the topic """
        try:
            if (value): # as long as value is not empty publishb
                self.producer.send(self.kafka_topic, value=value)
                self.producer.flush()
                print(f"Sent data to topic {self.kafka_topic}: {value}")
            else:
                print(f"Data {value} is empty")

            time.sleep(self.latency)

        except Exception as e:
            print("Error in sending data to Kafka, retying...")
            time.sleep(self.latency)
            self.start_stream_data(value) # sus nested functon call

if __name__ == "__main__":
    data_source = Data_source()
    data_source.start_stream_data()