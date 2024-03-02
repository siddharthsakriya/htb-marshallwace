from kafka import KafkaProducer
import time
import yfinance as yf

import json

class Data_source():
    def __init__(self, instrument_name='NVDA',topic_name='NVIDIA',config = "/Users/souparna/htb-marshallwace/oanda.cfg"):
        self.latency = 0.01
        self.config = config
        self.kafka_topic = topic_name
        self.bootstrap_servers = ['kafka:9093']
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers,api_version=(0,11,5),value_serializer=lambda x: json.dumps(x).encode('utf-8'))
        self.ticker_symbol = instrument_name
        self.tickerData = yf.Ticker(self.ticker_symbol)
    
    def on_success(self, time, bid, ask):
        message = {
            'time': time,
            'bid': bid,
            'ask': ask
        }
        self.producer.send(self.kafka_topic, value=message)
        print(f"Sent data to Kafka topic {self.kafka_topic}: {message}")

    def start_stream_data(self):
        """Streams data to Kafka."""
        while True:
            try:
                # data = self.api.stream_data(instrument=self.instruments)
                tickerDf = self.tickerData.history(period='1d')
                print(f"Data for {self.ticker_symbol}: {tickerDf['Close'].iloc[-1]}")
                if not(tickerDf.empty):
                    latest_price = tickerDf['Close'].iloc[-1]
                    self.producer.send(self.kafka_topic, value=latest_price)
                    self.producer.flush()
                    print(f"Sent data to topic {self.kafka_topic}: {latest_price}")
                else:
                    print(f"Data for {self.ticker_symbol} is empty")
                time.sleep(self.latency)
            except Exception as e:
                print("Error in sending data to Kafka, retying...")
                time.sleep(self.latency)
                continue

if __name__ == "__main__":
    data_source = Data_source()
    data_source.start_stream_data()