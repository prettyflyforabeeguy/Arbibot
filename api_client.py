#!/usr/bin/env python3
# This file is for making all API Calls to the various exchanges

import requests
import json
import credentials as _creds
import api_client as _api

class APIClient():
    def __init__(self):
        self.outputfile = ""
        self.method = ""
        self.headers = {}
        self.url = ""
        self.apikey = _creds.Creds().get_key()
        self.endpoint = _creds.Creds().get_endpoint()
        self.apisecret = _creds.Creds().get_secret()
        self.apisecret = bytes(self.apisecret, encoding='utf-8')
        self.cmcKey = _creds.Creds().get_cmckey()

    def api_call(self, method, apiName, url, requestBody):
        session = requests.Session()
        #session.headers.update(headers)
        try:
            if method == "GET":
                response = session.get(url)
                #print(response)
                data = json.loads(response.text)

            elif method == "POST":
                head = {'Content-Type' : 'application/x-www-form-urlencoded'}
                requestBody = {}
                response = session.post(url)
                #print(response)
                data = json.loads(response.text)

            else:
                print("Unsupported method")
        except Exception as e:
            data = response
            print(e)

        _api.APIClient().log_output(apiName, data)
        return data

    def log_output(self, apiName, data):
        filepath = "./data/" + apiName + ".json"
        try:
            with open(filepath, 'w') as outfile:
                json.dump(data, outfile)
        except:
            print("Failed to write to ./data")

    def timestamp(self, method):
        apiName = "servertimestamp"
        uri = self.endpoint + "/timestamp"
        response = _api.APIClient().api_call(method, apiName, uri, "")
        timestampList = response
        return timestampList

    def markets(self, method):
        apiName = "markets"
        uri = self.endpoint + "/markets"
        #No Auth required for this API call
        response = _api.APIClient().api_call(method, apiName, uri, "")
        marketsList = response
        return marketsList

    def ticker(self, method, coinSymbol, tradepair):
        apiName = "ticker"
        market = coinSymbol + tradepair
        uri = self.endpoint + "/tickers/" + market
        response = _api.APIClient().api_call(method, apiName, uri, "")
        tickerList = response
        return tickerList

    # All market trade pairs
    def members(self, method):
        apiName = "members"
        uri = self.endpoint + "/members/me"
        restapi = "/api/v2/members/me"
        query = ""
        sig, epoch = _creds.Creds().build_authentication(method, restapi, self.apikey, self.apisecret, query, "")
        url = uri + "?access_key=" + self.apikey + "&tonce=" + epoch + "&signature=" + sig + query
        response = _api.APIClient().api_call(method, apiName, url, "")
        membersList = response
        return membersList

    def depth(self, method, coinSymbol, tradepair):
        apiName = "depth"
        market = coinSymbol + tradepair
        uri = self.endpoint + "/depth?market=" + market
        response = _api.APIClient().api_call(method, apiName, uri, "")
        depthList = response
        return depthList

    # used for both checking open orders and posting new orders
    def orders(self, method, tradepair, state, limit, page, order_by, side, volume, price):
        market = tradepair
        try:
            if method == "GET":
                apiName = "orders"
                uri = self.endpoint + "/orders"
                query = "&market=" + market
                restapi = "/api/v2/orders"
                sig, epoch = _creds.Creds().build_authentication(method, restapi, self.apikey, self.apisecret, query, "")
                url = uri + "?access_key=" + self.apikey + "&tonce=" + epoch + "&signature=" + sig + query
                response = _api.APIClient().api_call(method, apiName, url, "")
                ordersList = response
                return ordersList

            elif method == "POST":
                apiName = "postOrder"
                uri = self.endpoint + "/orders"
                query1 = "&market=" + market + "&price=" + price + "&side=" + side 
                query2 = "&volume=" + volume

                restapi = "/api/v2/orders"
                sig, epoch = _creds.Creds().build_authentication(method, restapi, self.apikey, self.apisecret, query1, query2)
                url = uri + "?access_key=" + self.apikey + query1 + "&tonce=" + epoch + "&volume=" + volume + "&signature=" + sig
                #print(url)

                response = _api.APIClient().api_call(method, apiName, url, "")
                postordersList = response
                return postordersList
        except Exception as e:
            print(e)

    def cancelorders(self, method, side):
        apiName = "cancelOrder"
        uri = self.endpoint + "/orders/clear"
        restapi = "/api/v2/orders/clear"
        query = "&side=" + side
        sig, epoch = _creds.Creds().build_authentication(method, restapi, self.apikey, self.apisecret, query, "")
        url = uri + "?access_key=" + self.apikey + "&tonce=" + epoch + "&signature=" + sig + query 
        print(url)
        response = _api.APIClient().api_call(method, apiName, url, "")
        cancelordersList = response
        return cancelordersList

    def order_book(self, method, tradepair, ask_limit, bids_limit):
        market = tradepair
        apiName = market + "_order_book"
        uri = self.endpoint + "/order_book?market=" + market + "&ask_limit=" + str(ask_limit) + "&bids_limit=" + str(bids_limit)
        response = _api.APIClient().api_call(method, apiName, uri, "")
        orderbookList = response
        return orderbookList

    def trades(self, method, tradepair, limit, frm, to, order_by):
        market = tradepair
        apiName =  market + "_trades"
        #uri = self.endpoint + "/trades?market=" + market + "&limit=" + limit + "&timestamp=" + str(timestamp) + "&from=" + frm + "&to=" + to + "&order_by" + order_by
        uri = self.endpoint + "/trades?market=" + market + "&limit=" + limit
        response = _api.APIClient().api_call(method, apiName, uri, "")
        tradesList = response
        return tradesList

    # mytrades is order history, not open orders.
    def mytrades(self, method, tradepair, limit, timestmp, frm, to, order_by):
        # limit and other parameters don't seem to work
        market = tradepair
        apiName = market + "_mytrades"
        uri = self.endpoint + "/trades/my"
        query1 = "&market=" + market
        query2 = ""

        restapi = "/api/v2/trades/my"
        sig, epoch = _creds.Creds().build_authentication(method, restapi, self.apikey, self.apisecret, query1, query2)
        url = uri + "?access_key=" + self.apikey + query1 + "&tonce=" + epoch + "&signature=" + sig

        response = _api.APIClient().api_call(method, apiName, url, "")
        myTradesList = response
        return myTradesList

    # retrieve a deposit address for a given coin
    def deposit_address(self, method, currency):
        apiName = currency + "_depositaddress"
        uri = self.endpoint + "/deposit_address"
        restapi = "/api/v2/deposit_address"
        query = "&currency=" + currency
        sig, epoch = _creds.Creds().build_authentication(method, restapi, self.apikey, self.apisecret, query, "")
        url = uri + "?access_key=" + self.apikey + "&tonce=" + epoch + "&signature=" + sig + query  
        response = _api.APIClient().api_call(method, apiName, url, "")
        addressList = response
        return addressList

    def get_k(self, method, market):
        apiName = market + "_k"
        uri = self.endpoint + "/k?market=" + market
        response = _api.APIClient().api_call(method, apiName, uri, "")
        kList = response
        return kList

    def get_k_with_pending_trades(self, method, market, trade_id):
        apiName = market + "_kwpt"
        uri = self.endpoint + "/k_with_pending_trades?market=" + market + "&tradE_id=" + trade_id 
        response = _api.APIClient().api_call(method, apiName, uri, "")
        kList = response
        return kList

    # CoinMarketCap price quotes
    def cmc_Price_Quote(self, symbol, currency):
        apiName = symbol + "_cmcpricequote"
        uri = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?"
        url = uri + "symbol=" + symbol + "&convert=" + currency
        # Set headers
        headers = {
            "X-CMC_PRO_API_KEY" : self.cmcKey,
            "Accept" : "application/json"
        }
        # Request body
        requestBody = {
        }
        try:
            response = requests.get(url, headers=headers, data=requestBody)  #Execute the API and store the response.
            price = float(response.json()["data"][symbol]["quote"][currency]["price"])
        except Exception as e:
            print(e)
        return price

    # Crex24 Public API
    def get_Crex24Ticker(self, method, tradepair):
        apiName = tradepair + "_crex24ticker"
        uri = "https://api.crex24.com/v2/public/tickers?instrument="
        url = uri + tradepair
        response = _api.APIClient().api_call(method, apiName, url, "")
        return response

    # Xeggex Public API - Get Market by symbol
    def get_XeggexMarketSymbol(self, method, tradepair):
        apiName = tradepair + "_xeggexMarketSymbol"
        uri = "https://xeggex.com/api/v2"
        url = uri + "/market/getbysymbol/" + tradepair
        response = _api.APIClient().api_call(method, apiName, url, "")
        return response

if __name__ == '__main__':
    r = APIClient()
    # FOR TESTING
    #endpoint = Creds().get_endpoint()
    #apikey = Creds().get_key()
    #apisecret = Creds().get_secret()
    #apisecret = bytes(apisecret, encoding='utf-8')
    #apiName = "members"
    #restapi = "/api/v2/members/me"
    #method = "GET"
    #uri = endpoint + "/members/me"
    #sig, epoch = Creds().build_authentication(method, restapi, apikey, apisecret)
    #url = uri + "?access_key=" + apikey + "&tonce=" + epoch + "&signature=" + sig
    #print(url)
    #response = r.api_call(method, apiName, url)
    
    # TESTING INDIVIDUAL CALLS
    #response = r.markets("GET")
    #response = r.ticker("GET","ltc", "usdc")
    #response = r.ticker("GET","", "dimedoge")
    #response = r.members("GET")
    #response = r.depth("GET", "dime", "usdc")
    #response = r.order_book("GET", "dimeusdc", "", "1")
    #response = r.orders("GET", "dimeusdc", "", "10", "", "", "", "", "")
    #response = r.order_book("GET", "dimeusdc", 1, 10)
    ##response = r.orders("POST", "dimeusdc", "", "", "", "", "sell", "1.000", "0.00000998")
    #response = r.timestamp("GET")
    #response = r.trades("GET", "dimeusdc", "10", "", "", "")
    #response = r.cancelorders("POST", "buy")
    #response = r.mytrades("GET", "dimeusdc", "", "", "", "", "")
    #response = r.deposit_address("GET", "btc")
    #response = r.get_k("GET","dimebtc")
    #response = r.get_k_with_pending_trades("GET","dimebtc")
    response = r.cmc_Price_Quote("ETH", "USD")
    #response = r.get_Crex24Ticker("GET", "DIME-ETH")
    #response = r.get_XeggexMarketSymbol("GET", "DIME_DOGE")
    print(f"Test API result:\n{response}")
    #print(response["updatedAt"])
