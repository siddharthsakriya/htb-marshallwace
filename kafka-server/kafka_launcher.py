from kafka_producer import Data_source
from Financial_data_feeder import Data_fetcher
import os
import time
import yfinance as yf

ticker = os.getenv('TICKER')

data_source = Data_source("stock_data")

while True:
    
    data_source.start_stream_data(Data_fetcher(ticker).stream_data(), ticker)
    time.sleep(1)





