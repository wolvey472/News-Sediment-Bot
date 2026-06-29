#Web scraping
import requests as rq
import feedparser
import trafilatura
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

import pandas as pd


if tf.__version__:
    print("woprks")
else:
    print("NOT WORKING")

FEEDS = ["https://finance.yahoo.com/news/rssindex",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",            # CNBC top news
        "https://www.cnbc.com/id/20910258/device/rss/rss.html",             # CNBC markets
        "https://feeds.content.dowjones.io/public/rss/mw_topstories",       # MarketWatch
]

articles = []

for i in range(len(FEEDS)):
    rss_url = FEEDS[i]

    feed = feedparser.parse(rss_url)

    for entry in feed.entries:
        title = entry.get("title")
        link = entry.get("link")
        print("TITLE", title)
        print("LINK", link)

        html = trafilatura.fetch_url(link)

        if html is None: #no text
            print("could not get html")
            continue
        else: # we have text
            text = trafilatura.extract(html)
        
        articles.append({
            "source_feed":rss_url,
            "title":title,
            "link":link,
            "full_article":text
        })

df = pd.DataFrame(articles)

print(df.head())


        


   