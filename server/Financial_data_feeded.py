import yfinance as yf

class Datat_fetcher():
    def __init__(self, instrument='NVDA'):
        """
        This fetches the latest price for an instrument
        :param instrument: name of the instrument
        """

        self.ticker_symbol = instrument
        self.tickerData = yf.Ticker(self.ticker_symbol)
    def stream_data(self):
        """
        Fetches the Latest Prive for the above mentioned instrument
        :return: float ( price of instrument )
        """
        try:
            tickerDf = self.tickerData.history(period='1d')
            if not (tickerDf.empty):
                latest_price = tickerDf['Close'].iloc[-1] # this is the fetched price
                print(f"latest_price for {self.ticker_symbol} is {latest_price}")
                return latest_price
            else:
                print(f"Data for {self.ticker_symbol} is empty")
        except Exception as e:
            print("Error fetching Data")

if __name__ == "__main__":
    data = Datat_fetcher()
    data.stream_data()
