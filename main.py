#Web scraping
import requests as rq
import feedparser
import trafilatura
import re
#--------------

#Time
import time as t
from datetime import datetime, timezone as dt_timezone, timedelta

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
import openpyxl

#----------------

#Counting
from collections import Counter
import string
#----------------

#Looks
from pyfiglet import Figlet
import rich
from rich import print
from colorama import Fore
from rich.progress import track
#---------------

#API

#--------------

if tf.__version__:
    print("-"*20)
    print("WORKS")
    print("-"*20)
else:
    print("NOT WORKING")

FEEDS = ["https://finance.yahoo.com/news/rssindex",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",            # CNBC top news
        "https://www.cnbc.com/id/20910258/device/rss/rss.html",             # CNBC markets
        "https://feeds.content.dowjones.io/public/rss/mw_topstories",       # MarketWatch
]

FEEDS_TEST = [
    "https://finance.yahoo.com/news/rssindex",
]

FEEDS_MORE = [
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=AAPL,MSFT,NVDA,TSLA&region=US&lang=en-US",

    # Other finance feeds:
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://www.cnbc.com/id/20910258/device/rss/rss.html",
    "https://feeds.marketwatch.com/marketwatch/topstories/",
]



NCP_URL = (
    "https://finance.yahoo.com/xhr/ncp"
    "?location=US&queryRef=newsAll&serviceKey=ncp_fin"
    "&listName=latest-news&lang=en-US&region=US"
)

HEADERS = {
    "User-Agent": (     #These are only used so it dosent trace reqeuests/2.34
        "Mozilla/5.0  (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/126.0 Safari/537.36)"
    ),
    "Content-Type": "application/json",
}


f = Figlet(font="starwars", width=200)
ERR = f.renderText("ERROR")

C = 10 #default for ammt articles

articles=[]


   



def pull_data(count = int, session=None):
    articles.clear()
    cut_off = datetime.now(dt_timezone.utc) - timedelta(hours=24)
    
    http = session or rq # session only for tests

    json = {"serviceConfig": {
        "count":count,
        "snipperCount":count,
        "spaceId": "95993639",  
    }}

    resp = http.post(url=NCP_URL, json=json,
                      timeout=20, headers=HEADERS)

    #region ERR's
    resp.raise_for_status()
    if(code := resp.status_code()) in [400, 500]:
        print(ERR)
    
    if code in [401, 403, 501, 502]:
        print("Blocked?")

    if code == 429:
        print("[red]CODE Too many Requests")
    #endregion ERR's
    
    data = resp.json()

    stream = data["data"]["tickerStream"]["stream"]
    
    

    return stream

def get_link():
    
    stream = pull_data(count=C)

    

    #---check every possible link---

    if stream.get('clickThroughUrl'):
        link = stream['clickThroughUrl'].get("url")
    
    if link is None and stream.get("canonicalUrl"):
        link = stream["canonicalUrl"].get("url")
        
    if link and link.startswith("/"): 
        link = "https://finance.yahoo.com" + link
        #  safer to webscrape yahoo bc -> high traffic

    if link:
        return link
    if not link: #same as else
        return None
    

    

def web_scrapper(article_url):

    link = get_link()

    html = trafilatura.fetch_url(article_url)
    # dowload in html 
    if html is None:
        return None
    
    else:
        text = trafilatura.extract(html)

    return text


def main():

    print(f.renderText("-"*10))
    print(f.renderText("NEWS BOT"))
    print(f.renderText("-"*10))
    print("[bold black]- Carson Shae\n\n")

    web_scrapper()
   



file = "news.csv"
def log_data():

    stream = pull_data(count=10)

    if len(stream) == 0:
        print("[red]no articles found")
        return None
    
    df = pd.DataFrame(articles)

    #sort newest first

    if 'published' in df.columns:
        df['published'] = pd.to_datetime(df['published'], errors="coerce")
        df = df.sort_values('published', ascending=False)

    df.to_csv(file, index=False)

    print(f"Saved {len(df)} articles to {file}")
data = pull_data()

print("articles saved: ", len(data))

if __name__ == "__main__":
    main()
        

                    


    






    

    












        



   