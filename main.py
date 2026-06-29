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

articles = []
def web_scrapper():
    for i in range(len(FEEDS)):
        rss_url = FEEDS[i]

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
    find_stocks()
  


web_scrapper()

def train_model():
    ...
    
def find_stocks(text):
    if not isinstance(text, str):
        return []
    
    found = []

    for ticker, keywords in stocks.items():
        for word in keywords:
            pattern = r"\b" + re.escape(word) + r"\b"

            if re.search(pattern, text, re.IGNORECASE):
                found.append(ticker)
                break
    log_data()


def log_data():

    df = pd.DataFrame(articles)
    df.to_csv("text.csv",index=False)
    print(df.head())
    print(df.shape)
    columns = df.shape[0] # columns long
    text = df['full_article']

        


   