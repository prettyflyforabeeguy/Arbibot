# Arbibot
Arbitrage bot version 0.0.1 by <a href=https://github.com/prettyflyforabeeguy>prettyflyforabeeguy<a/><br>
This is a bot that checks exchange crypto prices and finds the cheapest trade pair.
Due to the inconsistency in which exchanges deal in fiat currencies, the Arbibot will use CoinMarketCap prices to make its price-per-coin comparisons.
This will mean there is a gap between actual prices and what you might see on the exchange.  Prices are meant to be an approximation only.
None of this is investing advice and you use this at your own risk.

<b>Getting Started:</b><br>
Make sure you have python 3.7 or greater installed <a href=https://www.python.org/downloads/>https://www.python.org/downloads/</a><br>
Clone this repo: ```git clone https://github.com/prettyflyforabeeguy/Arbibot.git ```
<br>
You will need to sign up for a free API Key from <a href=https://coinmarketcap.com/api/>CoinMarketCap</a><br>
This key will need to be added to your config/creds.json (see example below)<br>

     <b>Optional Settings:</b><br>
      If you create an account and setup an APIKey and APISecret from any of the supported exchanges below, You'll have the potential to make more complex queries in the future:   <br>
      <a href=https://c-patex.com>https://c-patex.com</a><br>
      <a href=https://crex24.com>https://crex24.com</a><br>
      <a href=https://xeggex.com/>https://xeggex.com</a><br>
     This key and secret will need to be added to your config/creds.json (see example below)<br>

It's important to know your API keys will have transaction limits and should not be abused.  So be mindful of how often you're instructing the bot to query prices.<br>
<br>
<b>config/config.json example:</b><br>
You will need to create a config.json file in the config folder using the example below.<br>
The fields have syntax restriction so please read the /config/CONFIG_READ.ME carefully for more details<br>
You can change the coin to any coin the exchange supports and include all the trade pairs you'd like compared.<br>
```
{
    "CheckFrequencyMinutes": "240",
    "Coin": "DIME",
    "CpatexEnabled": true,
    "TradePairs": [
        "dimeltc",
        "dimedoge",
        "dimeusdc"
    ],
    "Crex24Enabled": true,
    "CrexTradePairs":[
        "DIME-BTC",
        "DIME-ETH",
        "DIME-USDT"
    ],
    "XeggexEnabled": true,
    "XeggexTradePairs":[
        "DIME_USDT",
        "DIME_LTC",
        "DIME_DOGE"
    ]
}
```

<b>config/creds.json example:</b><br>
You will need to create a creds.json file in the config folder using the example below.<br>
At a minimum the CMCKey is required.  If you plan to use C-Patex the Cpatexendpoint is also required.
Please read the /config/CREDS_READ.ME carefully for more details<br>
Just populate your API Keys and API Secrets accordingly between the quotes<br>
```
{
    "Cpatexapi_key": "",
    "Cpatexapi_secret": "",
    "Cpatexendpoint": "https://c-patex.com:443/api/v2",
    "CMCKey": "",
    "crex24apikey": "",
    "crex24apisecret": "",
    "xeggexapikey": "",
    "xeggexapisecret": ""
}
```
<br>
Thank you all for your interest and support!<br>
If you found this or any of my projects useful and would like to see more in the future, please consider a donation:<br>
<b>DIME:</b> 7JwbNZdP3pzreem3v3rmWAXcP5LxvqRTgU <br>
<b>BTC:</b> bc1q3m4x0d8j6c8enkzeet2c4tcy26uflsm9s4njg4 <br>
<b>LTC:</b> ltc1qzhavlsq29kqe65cjjuq2l23d92f0mqlwkwldrg <br>
<b>ETH:</b> 0xaf9dB0Eaf3A398A4F549A09e1230B42B51FdAFF3 <br>

