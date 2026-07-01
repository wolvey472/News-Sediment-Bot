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
from api_key import API
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
FEEDS_TEST = ["https://finance.yahoo.com/news/rssindex",
]

url = "https://www.alphavantage.co/query"
stocks = {
    "AAPL": ["AAPL", "Apple"],
    "TSLA": ["TSLA", "Tesla"],
    "NVDA": ["NVDA", "Nvidia", "NVIDIA"],
    "MSFT": ["MSFT", "Microsoft"],
    "AMZN": ["AMZN", "Amazon"],
    "META": ["META", "Meta", "Facebook"],
    "GOOGL": ["GOOGL", "GOOG", "Google", "Alphabet"],
}


f = Figlet(font="starwars", width=200)
ERR = f.renderText("ERROR")


articles=[]

def pull_data():
    
    
    for rss_url in FEEDS_TEST: #CHANGE WHEN DONE TESTING
        print(f.renderText("-"*10))
        print(f.renderText("NEWS BOT"))
        print(f.renderText("-"*10))
        print("[bold black]- Carson Shae\n\n")
        t.sleep(2)     



        params= {    
            "apikey":API,
            "limit":"2",
            "function":"NEWS_SENTIMENT",
            "sort":"LATEST"
        }

        response = rq.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        for article in track(data['feed'], description="GETTING DATA "):
            title = article['title']
            sent_label = article['overall_sentiment_label']
            source = article['source']
            site_url = article['url']

            tickers=[]

       

        for te in article.get("ticker_sentiment", []):
            tickers.append({
                "ticker": te.get("ticker"),
                "relevance": te.get("relevance_score"),
                "sentiment_score": te.get("ticker_sentiment_score"),
                "sentiment_label": te.get("ticker_sentiment_label")
            })

        full_text = web_scrapper(site_url)

        articles.append({
            "title": title,
            "url": site_url,
            "source": source,
            "overall_sentiment": sent_label,
            "tickers": tickers,
            "full_article": full_text
        })





  
    


def web_scrapper(articles):

    for article in track(articles, description="SCRAPING "):

        if (html := trafilatura.fetch_url(article)) is not None:
            if (text := trafilatura.extract(html)) is not None:
                #found text
                store_text.append(text)
            else:
                continue
            print(ERR)
        else:
            continue
        print(ERR)
    return store_text





def log_data():
    df2 = pd.read_csv(r"C:\Users\carso\Downloads\CS50 Project NEW\sp500.csv")

    ticker = df2['Symbol']
    name = df2['Name']
    sector = df2['Sector']

    df = pd.DataFrame(articles)



    all_tickers = []
    all_companies = []
    title2 = []

    data_found = {"ticker":None,
                  "company":None,
                  "article":None}

    for article in track(articles, description="SEARCHING "):
        text = article["full_article"] #pull each text from each article
        if text is None: # should not run
            continue



        

                    


    


    #endregion
        

    ticker_counts = Counter(all_tickers)




    

    












        


def train_model():
    pass
    
pull_data()

   