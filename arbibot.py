#!/usr/bin/env python3
appversion = "0.0.4"
############################################################################
# This Arbitrage bot  application was created by prettyflyforabeeguy
# https://github.com/prettyflyforabeeguy
# Arbibot will query an exchange and all trade pairs of a given coin then
# it will compare the prices to CoinMarketCaps USD Price to understand which 
# trade pair is the cheapest.  Expect there will be a gap between CMC and 
# the Exchange Price.  The prices are an approximation.
# This is not investing advice.  Use at your own risk!

# When adding a new exchange and/or trade pairs don't forget to include them in appsettings.py and api_client.py
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
        self.xeggexEnabled = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "XeggexEnabled")
        self.xeggexPairs = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "XeggexTradePairs")
        self.stakecubeEnabled = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "StakecubeEnabled")
        self.stakecubePairs = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "StakecubeTradePairs")
        self.mercatoxEnabled = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "MercatoxEnabled")
        self.mercatoxPairs = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "MercatoxTradePairs")

    def get_cpatex_info(self, coin, timestamp, pricelist):
        # Create cpatextickers.csv new without column headers every time so it doesn't get bogged down with repeat data.
        exchange = "CPATEX"
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

                appc = float(sell) * price
                bppc = float(buy) * price
                #ppc = float(last) * price
                appc = f'{appc:.10f}'
                bppc = f'{bppc:.10f}'
                #sell = f'{sell:.10f}'
                each_pair = each_pair.upper()

                payload = [each_pair, at, buy, sell, low, high, last, vol, str(price), appc, bppc, exchange, str(timestamp)]
                #print(payload)
                _logger.Logger().write_to_csv("./data/ticker_history.csv", payload)
                _logger.Logger().write_to_csv("./data/cpatextickers.csv", payload)
                print(Style.BRIGHT + Fore.BLUE + f""" {each_pair}:\n   The lowest {c} sale price available on exchange: {sell}\n   This is approximately {appc} USD per coin.\n   Current CMC price for {c} is ${price}\n""")
            
            except Exception as e:
                print(f"Error in main_loop: {e}")

        ticker, lp = _logger.Logger().get_lowest_price("./data/cpatextickers.csv")
        ticker, hp = _logger.Logger().get_highest_price("./data/cpatextickers.csv")
        print(Style.BRIGHT + Fore.CYAN + Back.MAGENTA + f"The lowest ask is {ticker}: ${lp}")
        print(Style.DIM + Fore.BLACK + Back.WHITE + f"The highest bid is {ticker}: ${hp}")

    def get_mercatox_info(self, coin, timestamp, pricelist):
        # Create stakecubetickers.csv new without column headers every time so it doesn't get bogged down with repeat data.
        exchange = "MERCATOX"
        with open('./data/mercatoxmarketsymbol.csv', 'w', newline='') as file:
            fwriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print(Style.BRIGHT + Fore.WHITE + Back.GREEN + f"### MERCATOX {str(timestamp)} ###")
        ticker_all = _api.APIClient().get_MercatoxTicker("GET")
        for each_pair in self.mercatoxPairs:
            # Get target volume from trades
            try:
                ticker = _api.APIClient().get_MercatoxTradePair(each_pair, ticker_all)
                # Slice the coin pair for the price can be queried. Plus one for the underscore.
                clenght = len(coin) + 1
                c = each_pair[clenght:]
                c = c.upper()
                # Locate the CMC price for the coin in question
                for each in pricelist:
                    for k,v in each.items():
                        if k == str(c):
                            price = v

                at = timestamp
                buy = ticker[0]["highestBid"]
                sell = ticker[0]["lowestAsk"]
                low = ticker[0]["low24hr"]
                high = ticker[0]["high24hr"]
                last = ticker[0]["last_price"]
                vol = ticker[0]["base_volume"]
                appc = float(sell) * price
                appc = f'{appc:.10f}'
                if buy != None:
                    bppc = float(buy) * price
                    bppc = f'{bppc:.10f}'
                else:
                    bppc = "0.00"

                payload = [each_pair, at, buy, sell, low, high, last, str(vol), str(price), str(appc), str(bppc), exchange, str(timestamp)]
                _logger.Logger().write_to_csv("./data/ticker_history.csv", payload)
                _logger.Logger().write_to_csv("./data/mercatoxmarketsymbol.csv", payload)
                print(Style.BRIGHT + Fore.GREEN + f""" {each_pair}:\n   Current CMC price for {c} is ${price}\n   The lowest {c} sale (Ask) price available on exchange: {sell}\n   This is approximately {str(appc)} USD per coin.\n   ****************************** \n   The highest {c} buy (Bid) price available on exchange: {str(buy)}\n   This is approximately {str(bppc)} USD per coin.\n""")

            except Exception as e:
                print(f"Error in main_loop: {e}")

        ticker, lp = _logger.Logger().get_lowest_price("./data/mercatoxmarketsymbol.csv")
        ticker, hp = _logger.Logger().get_highest_price("./data/mercatoxmarketsymbol.csv")
        print(Style.DIM + Fore.BLACK + Back.WHITE + f"The lowest ask is {ticker}: ${str(lp)}")
        print(Style.DIM + Fore.BLACK + Back.WHITE + f"The highest bid is {ticker}: ${str(hp)}")

    def get_xeggex_info(self, coin, timestamp, pricelist):
        # Create xeggextickers.csv new without column headers every time so it doesn't get bogged down with repeat data.
        exchange = "XEGGEX"
        with open('./data/xeggexmarketsymbol.csv', 'w', newline='') as file:
            fwriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print(Style.DIM + Fore.BLUE + Back.BLUE + f"### XEGGEX {str(timestamp)} ###")
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

                #ppc = float(last) * price
                appc = float(sell) * price
                bppc = float(buy) * price
                appc = f'{appc:.14f}'
                buy = f'{buy:.14f}'
                sell = f'{sell:.14f}'
                bppc = f'{bppc:.14f}'

                payload = [each_pair, at, buy, sell, low, high, last, vol, str(price), appc, bppc, exchange, str(timestamp)]
                _logger.Logger().write_to_csv("./data/ticker_history.csv", payload)
                _logger.Logger().write_to_csv("./data/xeggexmarketsymbol.csv", payload)
                print(Style.BRIGHT + Fore.BLUE + f""" {each_pair}:\n   Current CMC price for {c} is ${price}\n   The lowest {c} sale (Ask) price available on exchange: {sell}\n   This is approximately {appc} USD per coin.\n   ****************************** \n   The highest {c} buy (Bid) price available on exchange: {buy}\n   This is approximately {bppc} USD per coin.\n""")


            except Exception as e:
                print(f"Error in main_loop: {e}")

        ticker, lp = _logger.Logger().get_lowest_price("./data/xeggexmarketsymbol.csv")
        ticker, hp = _logger.Logger().get_highest_price("./data/xeggexmarketsymbol.csv")
        print(Style.DIM + Fore.BLACK + Back.WHITE + f"The lowest ask is {ticker}: ${lp}")
        print(Style.DIM + Fore.BLACK + Back.WHITE + f"The highest bid is {ticker}: ${hp}")

    def get_stakecube_info(self, coin, timestamp, pricelist):
        # Create stakecubetickers.csv new without column headers every time so it doesn't get bogged down with repeat data.
        exchange = "STAKECUBE"
        with open('./data/stakecubemarketsymbol.csv', 'w', newline='') as file:
            fwriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print(Style.BRIGHT + Fore.WHITE + Back.CYAN + f"### STAKECUBE {str(timestamp)} ###")
        for each_pair in self.stakecubePairs:
            # Get target volume from trades
            try:
                ticker = _api.APIClient().get_StakeCubeMarketSymbol("GET", each_pair)
                ask, bid = _api.APIClient().get_StakeCubeBidAsk("GET", each_pair)
                # Slice the coin pair for the price can be queried. Plus one for the underscore.
                clenght = len(coin) + 1
                c = each_pair[clenght:]
                c = c.upper()
                # Locate the CMC price for the coin in question
                for each in pricelist:
                    for k,v in each.items():
                        if k == str(c):
                            price = v

                at = ticker["timestampConverted"]
                buy = bid
                sell = ask
                low = ticker["result"][each_pair]["low24h"]
                high = ticker["result"][each_pair]["high24h"]
                last = ticker["result"][each_pair]["lastPrice"]
                vol = ticker["result"][each_pair]["volumeTrade24h"]

                #ppc = float(last) * price
                appc = float(sell) * price
                bppc = float(buy) * price
                #appc = str(appc)
                appc = f'{appc:.10f}'
                buy = float(buy)
                buy = f'{buy:.10f}'
                sell = float(sell)
                sell = f'{sell:.10f}'
                bppc = float(bppc)
                bppc = f'{bppc:.10f}'

                payload = [each_pair, at, buy, sell, low, high, last, vol, str(price), appc, bppc, exchange, str(timestamp)]
                _logger.Logger().write_to_csv("./data/ticker_history.csv", payload)
                _logger.Logger().write_to_csv("./data/stakecubemarketsymbol.csv", payload)
                print(Style.BRIGHT + Fore.CYAN + f""" {each_pair}:\n   Current CMC price for {c} is ${price}\n   The lowest {c} sale (Ask) price available on exchange: {sell}\n   This is approximately {appc} USD per coin.\n   ****************************** \n   The highest {c} buy (Bid) price available on exchange: {buy}\n   This is approximately {bppc} USD per coin.\n""")

            except Exception as e:
                print(f"Error in main_loop: {e}")

        ticker, lp = _logger.Logger().get_lowest_price("./data/stakecubemarketsymbol.csv")
        ticker, hp = _logger.Logger().get_highest_price("./data/stakecubemarketsymbol.csv")
        print(Style.DIM + Fore.BLACK + Back.WHITE + f"The lowest ask is {ticker}: ${lp}")
        print(Style.DIM + Fore.BLACK + Back.WHITE + f"The highest bid is {ticker}: ${hp}")


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

                if self.mercatoxEnabled == True:
                    self.get_mercatox_info(self.coin, dt, pricelist)
                    print("")

                if self.xeggexEnabled == True:
                    self.get_xeggex_info(self.coin, dt, pricelist)
                    print("")

                if self.stakecubeEnabled == True:
                    self.get_stakecube_info(self.coin, dt, pricelist)
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

