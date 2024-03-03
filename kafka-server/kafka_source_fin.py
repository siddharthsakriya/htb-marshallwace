from kafka_producer import Data_source
from Financial_data_feeder import Data_fetcher
import os
import time
import yfinance as yf
import json

ticker = os.getenv('TICKER')

data_source = Data_source("stock_data")

while True:
    dic = {
        "stock_symbol": ticker,
        "price": Data_fetcher(ticker).stream_data(),
        "time_stamp": time.time()
    }
    json_data = json.dumps(dic) # publishes timed json data
    data_source.start_stream_data(json_data)
    time.sleep(1)





