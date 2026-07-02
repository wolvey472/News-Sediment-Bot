#Web scraping
import requests as rq
import feedparser
import trafilatura
import re
#--------------

#Time
import time as t
from datetime import datetime, timedelta
from time import timezone
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
def get_feed_entries(rss_url):
    response = rq.get(rss_url, headers=HEADERS, timeout=15)

    print("RSS:", rss_url)
    print("Status:", response.status_code)

    if response.status_code != 200:
        print("[red] FEED ERROR")
        return []
        

    feed = feedparser.parse(response.content)
    print("Feed count:", len(feed.entries))

    return feed.entries

def entry_datetime(entry):
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

    if hasattr(entry, "updated_parsed") and entry.updated_parsed:
        return datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
    
    return None #if no time (shouldent happen)

def pull_data():
    articles.clear()
    cut_off = datetime.now() - timedelta(hours=24)
    
    for rss_url in FEEDS_TEST: #CHANGE WHEN DONE TESTING
        print(f.renderText("-"*10))
        print(f.renderText("NEWS BOT"))
        print(f.renderText("-"*10))
        print("[bold black]- Carson Shae\n\n")
        t.sleep(2)     



    for rss_url in FEEDS_TEST: #CHANGE WHEN DONE TESTING
        print(f.renderText("-"*10))
        print(f.renderText("NEWS BOT"))
        print(f.renderText("-"*10))
        print("[bold black]- Carson Shae\n\n")
        t.sleep(2)

        entries = get_feed_entries(rss_url)


        for entry in track(entries, description="SCRAPING "):
            title = entry.get("title")
            link = entry.get("link")
            published_time = entry_datetime(entry)

            #print("CHECKING: ", title)
            print()
            print(title)
            print(published_time)
            print(link)


            if (published_time is None) or (published_time < cut_off):
                print("[bold blue] SKIPPED DUE TO DATE")
                continue
            if not link:
                continue

            html = trafilatura.fetch_url(link)

            if html is None: #no text
                print("NO TEXT FOUND")
                continue

            text = trafilatura.extract(html)

            if not text:
                print("EXTRACT FAILED")
                continue
                

            articles.append({       #data appending
                "source_feed":rss_url,
                "title":title,
                "link":link,
                "full_article":text
            })
    
    print("articles saved: ",len(articles))
    log_data()





  
    


def web_scrapper(article_url):

    html = trafilatura.fetch_url(article_url)

    if html is None:
        print(f"[red]No HTML found for:[/red] {article_url}")
        return None

    text = trafilatura.extract(html)

    if text is None:
        print(f"[red]No article text found for:[/red] {article_url}")
        return None

    return text





def log_data():
    df = pd.DataFrame(articles)

    print(df[["title", "source", "overall_sentiment", "url"]])

    df.to_csv("news_articles.csv", index=False)

    print("[green]Saved to news_articles.csv[/green]")

    ticker_count = Counter()

pull_data()


        

                    


    






    

    












        



   