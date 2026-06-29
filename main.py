#Web scraping
import requests as rq
import feedparser
import trafilatura
import re
#--------------

#Time
import time as t
from datetime import datetime
#--------------

#Machine Learning
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"   # hide INFO/WARNING/ERROR C++ logs
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # hide the oneDNN message
import tensorflow as tf
#---------------

#numbers helpers
import pandas as pd
import numpy as np
#----------------

if tf.__version__:
    print("woprks")
else:
    print("NOT WORKING")

FEEDS = ["https://finance.yahoo.com/news/rssindex",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",            # CNBC top news
        "https://www.cnbc.com/id/20910258/device/rss/rss.html",             # CNBC markets
        "https://feeds.content.dowjones.io/public/rss/mw_topstories",       # MarketWatch
]
stocks = {
    "AAPL": ["AAPL", "Apple"],
    "TSLA": ["TSLA", "Tesla"],
    "NVDA": ["NVDA", "Nvidia", "NVIDIA"],
    "MSFT": ["MSFT", "Microsoft"],
    "AMZN": ["AMZN", "Amazon"],
    "META": ["META", "Meta", "Facebook"],
    "GOOGL": ["GOOGL", "GOOG", "Google", "Alphabet"],
}


import re

def extract_yahoo_tickers(text):
    if not isinstance(text, str):
        return []

    pattern = r"\((NYSE|NASDAQ|AMEX|NYSEAMERICAN|OTC|OTCMKTS):\s*([A-Z][A-Z0-9.-]*)\)"

    matches = re.findall(pattern, text)

    results = []

    for exchange, ticker in matches:
        results.append({
            "exchange": exchange,
            "ticker": ticker
        })

    return results


articles = []
def web_scrapper():
    articles.clear() #make sure none is in the list

    for rss_url in FEEDS:


        feed = feedparser.parse(rss_url)

        for entry in feed.entries:
            title = entry.get("title")
            link = entry.get("link")

            print("CHECKING: ", title)

            html = trafilatura.fetch_url(link)

            if html is None: #no text
                print("NO TEXT FOUND")
                continue
            else: # we have text
                text = trafilatura.extract(html)
                print("TEXT FOUND")
            
            articles.append({
                "source_feed":rss_url,
                "title":title,
                "link":link,
                "full_article":text
            })
    log_data()
  







def log_data():

    df = pd.DataFrame(articles)

    df["stocks_mentioned"] = df["full_article"].apply(extract_yahoo_tickers)

    df.to_csv("text.csv",index=False)
    print(df.head())
    print(df[["title", "stocks_mentioned"]].head())
    print(df.shape)


    #Might need these for Neural netowrk data
    columns = df.shape[0] # columns long
    text = df['full_article']

def train_model():
    pass
    
web_scrapper()

   