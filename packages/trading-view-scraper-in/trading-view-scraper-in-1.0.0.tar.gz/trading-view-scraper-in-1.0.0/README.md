Trading view scraper in is a python library to scrape data from the trading view website. 
It currently runs only on windows.

## Scrape Trading View
In this, we first import library using simple commands
```sh
from trading_view_scraper_in import *
response=trading.view_market_indices()
```

### Response Data

```json
        "stock": "Dow 30",
        "link": "https://in.tradingview.com/symbols/DJ-DJI/",
        "price": "35911.82",
        "price_change": "\u2212201.81",
        "price_change_percent": "\u22120.56%"
```
#### BotStudio
[Bot_Studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up in which trading view page is loaded and scrapes the data from the page.


### Installation

```sh
pip install trading-view-scraper-in
```

### Import
```sh
from trading_view_scraper_in import *
```

###  Get indices
```sh
response=trading.view_market_indices()
```

### Run bot on cloud
You can run bot on [Cloud](https://datakund.com/products/trading-view-market-indices).

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

