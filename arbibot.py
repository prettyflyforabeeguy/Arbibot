#!/usr/bin/env python3
appversion = "0.0.3"
############################################################################
# This Arbitrage bot  application was created by prettyflyforabeeguy
# https://github.com/prettyflyforabeeguy
# Arbibot will query an exchange and all trade pairs of a given coin then
# it will compare the prices to CoinMarketCaps USD Price to understand which 
# trade pair is the cheapest.  Expect there will be a gap between CMC and 
# the Exchange Price.  The prices are an approximation.
# This is not investing advice.  Use at your own risk!
###########################################################################

import appsettings as _appsettings
import api_client as _api
import logger as _logger
import sys, datetime, csv, time
from colorama import Fore, Back, Style, init

init(autoreset=True) 

class ArbiBot():
    def __init__(self):
        self.appsettings_dict = _appsettings.AppSettings().appsettings_dict
        self.chkfreq = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "CheckFrequencyMinutes")
        self.coin = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "Coin")
        self.cpatexEnabled = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "CpatexEnabled")
        self.cpatexPairs = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "CpatexTradePairs")
        self.crex24Enabled = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "Crex24Enabled")
        self.crexPairs = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "CrexTradePairs")
        self.xeggexEnabled = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "XeggexEnabled")
        self.xeggexPairs = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "XeggexTradePairs")

    def get_cpatex_info(self, coin, timestamp, pricelist):
        # Create cpatextickers.csv new without column headers every time so it doesn't get bogged down with repeat data.
        with open('./data/cpatextickers.csv', 'w', newline='') as file:
            fwriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print(Style.BRIGHT + Fore.CYAN + Back.MAGENTA + f"### C-PATEX {str(timestamp)} ###")
        for each_pair in self.cpatexPairs:
            # Get target volume from trades
            try:
                ticker = _api.APIClient().ticker("GET", "", each_pair)
                # Slice the coin pair for the price can be queried.
                clenght = len(coin)
                c = each_pair[clenght:]
                c = c.upper()
                # Locate the CMC price for the coin in question
                for each in pricelist:
                    for k,v in each.items():
                        if k == str(c):
                            price = v

                at = ticker["at"]
                buy = ticker["ticker"]["buy"]
                sell = ticker["ticker"]["sell"]
                low = ticker["ticker"]["low"]
                high = ticker["ticker"]["high"]
                last = ticker["ticker"]["last"]
                vol = ticker["ticker"]["vol"]

                ppc = float(last) * price
                ppc = f'{ppc:.10f}'
                #sell = f'{sell:.10f}'
                each_pair = each_pair.upper()

                payload = [each_pair, at, buy, sell, low, high, last, vol, str(price), ppc]
                #print(payload)
                _logger.Logger().write_to_csv("./data/ticker_history.csv", payload)
                _logger.Logger().write_to_csv("./data/cpatextickers.csv", payload)
                print(Style.BRIGHT + Fore.BLUE + f""" {each_pair}:\n   The lowest {c} sale price available on exchange: {sell}\n   This is approximately {ppc} USD per coin.\n   Current CMC price for {c} is ${price}\n""")
            
            except Exception as e:
                print(f"Error in main_loop: {e}")

        ticker, lp = _logger.Logger().get_lowest_price("./data/cpatextickers.csv")
        print(Style.BRIGHT + Fore.CYAN + Back.MAGENTA + f"The lowest purchase price is {ticker}: ${lp}")
    
    def get_crex24_info(self, coin, timestamp, pricelist):
        # Create crex24tickers.csv new without column headers every time so it doesn't get bogged down with repeat data.
        with open('./data/crex24tickers.csv', 'w', newline='') as file:
            fwriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print(Style.BRIGHT + Fore.WHITE + Back.CYAN + f"### CREX24 {str(timestamp)} ###")
        for each_pair in self.crexPairs:
            # Get target volume from trades
            try:
                ticker = _api.APIClient().get_Crex24Ticker("GET", each_pair)
                # Slice the coin pair for the price can be queried. Plus one for the dash symbol.
                clenght = len(coin) + 1
                c = each_pair[clenght:]
                c = c.upper()
                # Locate the CMC price for the coin in question
                for each in pricelist:
                    for k,v in each.items():
                        if k == str(c):
                            price = v

                at = ticker[0]["timestamp"]
                buy = ticker[0]["bid"]
                sell = ticker[0]["ask"]
                low = ticker[0]["low"]
                high = ticker[0]["high"]
                last = ticker[0]["last"]
                vol = ticker[0]["volumeInUsd"]

                ppc = float(last) * price
                ppc = f'{ppc:.10f}'
                sell = f'{sell:.10f}'

                payload = [each_pair, at, buy, sell, low, high, last, vol, str(price), ppc]
                #payload = [each_pair, at, buy, sell, low, high, last, vol]
                #print(payload)
                _logger.Logger().write_to_csv("./data/ticker_history.csv", payload)
                _logger.Logger().write_to_csv("./data/crex24tickers.csv", payload)
                print(Style.BRIGHT + Fore.BLUE + f""" {each_pair}:\n   The lowest {c} sale price available on exchange: {sell}\n   This is approximately {ppc} USD per coin.\n   Current CMC price for {c} is ${price}\n""")
            
            except Exception as e:
                print(f"Error in main_loop: {e}")
        
        ticker, lp = _logger.Logger().get_lowest_price("./data/crex24tickers.csv")
        print(Style.BRIGHT + Fore.WHITE + Back.CYAN + f"The lowest purchase price is {ticker}: ${lp}")

    def get_xeggex_info(self, coin, timestamp, pricelist):
        # Create crex24tickers.csv new without column headers every time so it doesn't get bogged down with repeat data.
        with open('./data/xeggexmarketsymbol.csv', 'w', newline='') as file:
            fwriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print(Style.DIM + Fore.BLACK + Back.WHITE + f"### XEGGEX {str(timestamp)} ###")
        for each_pair in self.xeggexPairs:
            # Get target volume from trades
            try:
                ticker = _api.APIClient().get_XeggexMarketSymbol("GET", each_pair)
                # Slice the coin pair for the price can be queried. Plus one for the underscore.
                clenght = len(coin) + 1
                c = each_pair[clenght:]
                c = c.upper()
                # Locate the CMC price for the coin in question
                for each in pricelist:
                    for k,v in each.items():
                        if k == str(c):
                            price = v

                at = ticker["updatedAt"]
                buy = ticker["bestBidNumber"]
                sell = ticker["bestAskNumber"]
                low = ticker["lowPrice"]
                high = ticker["highPriceNumber"]
                last = ticker["lastPriceNumber"]
                vol = ticker["volumeUsdNumber"]

                ppc = float(last) * price
                ppc = f'{ppc:.10f}'
                sell = f'{sell:.10f}'
                
                payload = [each_pair, at, buy, sell, low, high, last, vol, str(price), ppc]
                _logger.Logger().write_to_csv("./data/ticker_history.csv", payload)
                _logger.Logger().write_to_csv("./data/xeggexmarketsymbol.csv", payload)
                print(Style.BRIGHT + Fore.BLUE + f""" {each_pair}:\n   The lowest {c} sale price available on exchange: {sell}\n   This is approximately {ppc} USD per coin.\n   Current CMC price for {c} is ${price}\n""")

            except Exception as e:
                print(f"Error in main_loop: {e}")
        
        ticker, lp = _logger.Logger().get_lowest_price("./data/xeggexmarketsymbol.csv")
        print(Style.DIM + Fore.BLACK + Back.WHITE + f"The lowest purchase price is {ticker}: ${lp}")    

    def main_loop(self, chkfreq, unique_pairs):
        while True:
            try:
                print("Getting Coin Market Cap prices...")
                pricelist = _api.APIClient().get_CMC_Prices(unique_pairs, "USD")
                #print(pricelist)

            except Exception as e:
                print(f"There was an issue getting Coin Market Cap prices:\n {e}")
                print("Shutting down Arbibot...")
                sys.exit(0)
            
            try:
                dt = datetime.datetime.now()
                if self.cpatexEnabled == True:
                    self.get_cpatex_info(self.coin, dt, pricelist)
                    print("")
                
                if self.crex24Enabled == True:
                    self.get_crex24_info(self.coin, dt, pricelist)
                    print("")

                if self.xeggexEnabled == True:
                    self.get_xeggex_info(self.coin, dt, pricelist)
                    print("")

                appStartTimeStamp = str(datetime.datetime.now())
                print(f"{appStartTimeStamp}")
                t = chkfreq / 60
                print(f"Waiting for {float(t)} minute(s) before checking prices again...")
                time.sleep(chkfreq) 

            except Exception as e:
                print(f"Exception in main_loop: {e}")
                sys.exit(0)

    def startup(self, chkfreq):
        appStartTimeStamp = str((datetime.datetime.now()))
        print(f"Starting up Arbibot...\n{appStartTimeStamp}")
        appStart_text = f"""
    Based on your config.json configuration:
    Arbibot will check {self.coin} prices every {float(chkfreq)} minute(s)..."""
        
        print(appStart_text)
        print("")
        time.sleep(2)
        # Multiply the checkfreq because the sleep statement is in milliseconds. 
        chkfreq = float(chkfreq) * 60
        # Create initial CSV files
        _logger.Logger().create_csv("./data/ticker_history.csv")

        unique_pairs = _appsettings.AppSettings().get_unique_trade_pairs()

        self.main_loop(chkfreq, unique_pairs)


if __name__ == '__main__':
    ab = ArbiBot()
    try:
        ab.startup(ab.chkfreq)
    except SystemExit:
        pass

