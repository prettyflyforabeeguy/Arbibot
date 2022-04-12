#!/usr/bin/python3

import telebot
import credentials as _creds
import logger as _logger
import json
import datetime, time

API_TOKEN = _creds.Creds().get_tgramkey()
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi, I am DimePriceBot.\nI can can lookup DIME prices for all trade pairs on the supported exchanges.  All prices should be considered as an approximation because the USD prices are made in comparison to Coin Market Cap and may not be an exact match to the exchange.  However it will be very close.
I only update prices every 8 hours so frequent checking of prices will not result in new information.
If you're enjoying this service and would like help keep it going, consider a DIMECOIN donation: 7JwbNZdP3pzreem3v3rmWAXcP5LxvqRTgU

Type the /help command for more options.\
""")

@bot.message_handler(commands=['help'])
def help(message):
    #msg = "My available commands are: \n/pricecheckall \n/cpatex \n/crex24 \n/xeggex"
    msg = "My available commands are: \n/saleprices   for the lowest prices DIME is for sale on all exchanges.\n/buyprices  for the highest prices DIME can be bought for on all exchanges.\nTo see a summary of all trade pairs on a given exchange type summary <exchange>.  No forward slash.  e.g summary cpatex  summary crex24   or summary xeggex"

    bot.reply_to(message, msg)

@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "Hello!")


@bot.message_handler(commands=['saleprices'])
def saleprices(message):
    dt =  str(datetime.datetime.now())
    fname = './data/cpatextickers.csv'
    fname2 = './data/crex24tickers.csv'
    fname3 = './data/xeggexmarketsymbol.csv'

    cp_coin, cp_price = _logger.Logger().get_lowest_price(fname)
    cr_coin, cr_price = _logger.Logger().get_lowest_price(fname2)
    xe_coin, xe_price = _logger.Logger().get_lowest_price(fname3)

    cpatex = "C-PATEX: " + cp_coin + " " + cp_price
    crex = "CREX24: " + cr_coin + " " + cr_price
    xeggex = "XEGGEX: " + xe_coin + " " + xe_price

    prices = dt + "\n" + "Lowest DIME sale prices on:\n" + "    " + cpatex + "\n" + "    " + crex + "\n" + "    " + xeggex + "\n"
    bot.send_message(message.chat.id, prices)

@bot.message_handler(commands=['buyprices'])
def buyprices(message):
    dt =  str(datetime.datetime.now())
    fname = './data/cpatextickers.csv'
    fname2 = './data/crex24tickers.csv'
    fname3 = './data/xeggexmarketsymbol.csv'

    cp_coin, cp_price = _logger.Logger().get_highest_price(fname)
    cr_coin, cr_price = _logger.Logger().get_highest_price(fname2)
    xe_coin, xe_price = _logger.Logger().get_highest_price(fname3)

    cpatex = "C-PATEX: " + cp_coin + " " + cp_price
    crex = "CREX24: " + cr_coin + " " + cr_price
    xeggex = "XEGGEX: " + xe_coin + " " + xe_price

    prices = dt + "\n" + "Highest DIME buy prices on:\n" + "    " + cpatex + "\n" + "    " + crex + "\n" + "    " + xeggex + "\n"
    bot.send_message(message.chat.id, prices)

def summary(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() not in "summary":
        return False
    else:
        return True

@bot.message_handler(func=summary)
def cpatex(message):
    request = message.text.split()[1]
    if request == "cpatex":
        exchange = 'C-Patex'
        csvfile = './data/cpatextickers.csv'
        validExchange = True
    elif request == 'crex24':
        exchange = 'CREX24'
        csvfile = './data/crex24tickers.csv'
        validExchange = True
    elif request == 'xeggex':
        exchange = "XeggeX"
        csvfile = './data/xeggexmarketsymbol.csv'
        validExchange = True
    else:
        validExchange = False
        bot.send_message(message.chat.id, "Exchange not found!")

    if validExchange == True:
        pricelist = _logger.Logger().get_exchange_details(csvfile, exchange)
        for each in pricelist:
            bot.send_message(message.chat.id, each)
            time.sleep(.5)

        lcoin, llowest = _logger.Logger().get_lowest_price(csvfile)
        lp = f"The lowest ask price for  {exchange} is {lcoin} at {llowest} USD"
        hcoin, hhighest = _logger.Logger().get_highest_price(csvfile)
        hp = f"The highest bid price for {exchange} is {hcoin} at {hhighest} USD"

        reply = lp + "\n" + hp
        bot.send_message(message.chat.id, reply)




bot.polling()

