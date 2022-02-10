# Arbibot
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
You will need an account and APIKey and APISecret from at least one of these exchanges:<br>
<a href=https://c-patex.com>https://c-patex.com</a><br>
<a href=https://crex24.com>https://crex24.com</a><br>
<a href=https://xeggex.com/>https://xeggex.com/</a>
This key and secret will need to be added to your config/creds.json (see example below)<br>
It's important to know your API keys will have transaction limits and should not be abused.  So be mindful how often you're instructing the bot to query prices.<br>
<br>
<b>config/config.json example:</b><br>
see the /config/CONFIG_READ.ME for more details<br>
You can change the coin to any coin the exchange supports and include all the trade pairs you'd like compared.
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
