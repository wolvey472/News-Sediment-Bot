#Web scraping
import requests as rq
import feedparser
import trafilatura
import re
#--------------

#Time
import time as t
from datetime import datetime, timezone as dt_timezone, timedelta
from zoneinfo import ZoneInfo
#--------------

#Machine Learning
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"   # hide INFO/WARNING/ERROR C++ logs
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # hide the oneDNN message
import tensorflow as tf
from finBERT_model import analyze_text
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



#NCP_URL = "https://finance.yahoo.com/xhr/ncp"
NCP_URL = (
    "https://finance.yahoo.com/xhr/ncp"
    "?location=US&queryRef=newsAll&serviceKey=ncp_fin"
    "&listName=latest-news&lang=en-US&region=US")

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
WAIT_TIME = 90 #seconds for time to wait
FILE = 'news.csv'

LIVE = False  #set to false for past
# set to true for live checking

articles=[]


   



def pull_data(count = 10, session=None):

    cut_off = datetime.now(dt_timezone.utc) - timedelta(hours=24)
    
    http = session or rq # session only for tests

    json = {"serviceConfig": {
        "count":count,
        "snippetCount":count,
        "spaceId": "95993639",
      
    }}

    resp = http.post(url=NCP_URL, json=json,
                      timeout=20, headers=HEADERS)

    #region ERR's
    
    if resp.status_code != 200:
        print("BAD REQUESTS")
        print(resp.status_code)
        print(resp.url)
        print(resp.text[:500])
        return []
    
    if code:= resp.status_code in [401, 403, 501, 502]:
        print("[red]Blocked?")

    if code == 429:
        print("[red]CODE Too many Requests")
   
    #endregion ERR's
    
    data = resp.json()

    stream = data["data"]["tickerStream"]["stream"]
    
    #print(stream)

    return stream
def get_date(article):
    dt = article['content']['pubDate']

    utc_time = datetime.fromisoformat(dt)
    

    ct = utc_time.astimezone(ZoneInfo("America/Chicago"))
    normal_time = ct.strftime("%I:%M %p")
    print(normal_time)
    return normal_time

def get_ticker(article):
    ticker = None
    try:
        ticker = article['content']['finance']['stockTickers']
    except: 
        return None
    else:
        return ticker

def get_link(article):
    
    link = None
    
    link = article['content']['canonicalUrl']['url']
    print(link)
    return link
    
def get_title(article):
    if title :=article.get("title"):
        return title
    else:
        print("NO title found")
        return None

    

def web_scrapper(article_url):

    html = trafilatura.fetch_url(article_url)
    # dowload in html 
    if html is None:
        return None
    
    else:
        text = trafilatura.extract(html)
    if text:
        return text

def run_model():
    ...

def save_articles(article,pos_tickers,neg_tickers,conclusion):
    df = pd.DataFrame([article, pos_tickers, neg_tickers, conclusion])
    df.to_csv(FILE, index=False)
    print(f"saved {len(article)} articles to {FILE}")
    print(df.head())

seen_tickers=[]
positive_tickers=[]
negative_tickers=[]
def main():

    print(f.renderText("-"*10))
    print(f.renderText("NEWS BOT"))
    print(f.renderText("-"*10))
    print("[bold black]- Carson Shae\n\n")

    stream = pull_data(count=C, session=None)
    for article in stream:
        date = get_date(article=article)
        link_ = get_link(article=article)
        txt = web_scrapper(link_)
        ticker = get_ticker(article=article)
        if ticker is not None and txt is not None:
            conclusion = analyze_text(txt)
            print(f"Conclusion {conclusion['conclusion']}")
            for symbol in ticker:
                symbols = symbol['symbol']
                print(symbols)
                seen_tickers.append(symbols)
                if conclusion['conclusion'] == 'positive':
                    positive_tickers.append(symbols)
                if conclusion['conclusion'] == 'negative':
                    negative_tickers.append(symbols)
                sum = {"article":article, 
                       "pos_tickers":positive_tickers,
                          "neg_tickers":negative_tickers,  #this dont work
                        "conclusion":conclusion,
                        }


   






if __name__ == "__main__":
    main()
        

                    


    






    

    












        



   