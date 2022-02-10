# This file is for reading and writing to the csv data files
import csv
import os
from datetime import datetime

class Logger():
    def __init__(self):
        self.ticker_history_csv = "./data/ticker_history.csv"
        self.tickers_columnheaders = ["coin", "at", "ticker", "buy", "sell", "low", "high", "last","vol", "coinUSDprice", "pricePerCoin"]

    def create_csv(self, csvfile):
        if os.path.isfile(csvfile):
            pass
        else:
            try:
                if csvfile == self.ticker_history_csv:
                    with open(csvfile, 'w', newline='') as file:
                        fwriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        fwriter.writerow(self.tickers_columnheaders)
            except IOError:
                print(f"Error: Unable to create {csvfile}")
    
    def write_to_csv(self, csvfile, payload):
        try:
            with open(csvfile, 'a', newline='') as file:
                fwriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                fwriter.writerow(payload)
        except IOError:
            print(f"Error: Unable to write to {csvfile}")

    def get_lowest_price(self, csvfile):
        price_list = []
        coin = ""
        try:
            with open(csvfile) as f:
                contents_of_f = csv.reader(f)
                for row in contents_of_f:
                    #price_list.append(float(row[9]))
                    price_list.append(row[9])
        
            lowest = min(price_list)
        except Exception as e:
            print(f"{e}")

        try:
            with open(csvfile) as f:
                contents_of_f = csv.reader(f)
                # get the coin sysmbol for the lowest price
                for row in contents_of_f:
                    if row[9] == lowest:
                        coin = row[0]
        except Exception as e:
            print(f"{e}")

        return coin, lowest

if __name__ == '__main__':
    log = Logger()
    timestamp = datetime.now()
    #ticker, lp = log.get_lowest_price("./data/tickers.csv")
    #print(f"{ticker}: {lp}")