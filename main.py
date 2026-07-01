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



articles = []
def web_scrapper():
    articles.clear() #make sure none is in the list
    
    for rss_url in FEEDS_TEST: #CHANGE WHEN DONE TESTING
        print(f.renderText("-"*10))
        print(f.renderText("NEWS BOT"))
        print(f.renderText("-"*10))
        print("[bold black]- Carson Shae\n\n")
        t.sleep(2)     

        params= {    
            "apikey":API,
            "limit":"20",
            "function":"NEWS_SENTIMENT",
            "sort":"LATEST"
        }

        response = rq.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        for article in track(data, description="SCRAPING"):
            title = article['title']
            sent_label = ['overall_sentiment_label']

            for t in article['ticker_sentiment']:
                ticker = t['ticker']
                relevance = t['relevance_score']
                sent_score = ['ticker_sentiment_score']



            articles.append({       #data appending
                "source_feed":rss_url,
                "title":title,
                "link":link,
                "full_article":text
            })
    log_data()



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


    #region TICKER AND COMPANY SEARCHES
    #   --- TICKER ---
        for word in text.split():

            m = re.search(r"\(([A-Z]+):([A-Z.]+)\)", word)
            if m is not None:
                exchange = m.group(1)   # "NYSE"
                nw = m.group(2)         # "NVDA"
                #print(nw)
                if all_tickers:
                    if nw not in all_tickers[-1]:
                        all_tickers.append(nw)
                else:
                    all_tickers.append(nw) #append first no matter what

    #   --- COMPANIES ---
        valid = ["inc.", "corp.", "inc", "co", "group", "corporation", "systems"]  
        companies = name #Valid DF companies

        def clean_text(text):
            return text.translate(str.maketrans("", "", string.punctuation)).lower()

        clean_txt = clean_text(text)

        for company in companies:
            clean_company = clean_text(company)

            if clean_company in clean_txt:
                #print("FOUND:", company)
                all_companies.append(company)
                title2.append(text)
        

                    


    


    #endregion
        

    ticker_counts = Counter(all_tickers)




    

    












        


def train_model():
    pass
    
web_scrapper()

   