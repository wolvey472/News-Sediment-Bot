#region IMPORT
#Web scraping
import requests as rq
import feedparser
import trafilatura
#--------------

#Time
import time as t
from datetime import datetime, timezone as dt_timezone, timedelta
from zoneinfo import ZoneInfo
#--------------

#Machine Learning
from finBERT_model import analyze_text
#---------------

#numbers helpers
import pandas as pd
import random as rd
#----------------

#Counting
from collections import Counter
#----------------

#Looks
from pyfiglet import Figlet
from rich import print
from colorama import Fore
from rich.progress import track
#---------------
#endregion IMPORT


#------------------------------
#NCP_URL = "https://finance.yahoo.com/xhr/ncp" #old -> dont use
NCP_URL = (
    "https://finance.yahoo.com/xhr/ncp"
    "?location=US&queryRef=newsAll&serviceKey=ncp_fin"
    "&listName=latest-news&lang=en-US&region=US")
#------------------------------

#------------------------------
HEADERS = {
    "User-Agent": (     #These are only used so it dosent trace reqeuests/2.34
        "Mozilla/5.0  (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/126.0 Safari/537.36)"
    ),
    "Content-Type": "application/json",
}
#------------------------------

#------------------------------
f = Figlet(font="starwars", width=200)
ERR = f.renderText("ERROR")
STOPPED = f.renderText("STOPPED")
#------------------------------

#------------------------------
LIVE = True  
#set to false for past
# set to true for live checking
#------------------------------

#------------------------------
LOWER = 30 #lower limit for time in between rq
UPPER = 40 # upper limit
# used to randomly send requests -> seem less like a bot
#------------------------------

#------------------------------
C = 30 #default for ammt articles
if LIVE == True:
    C = 1
#------------------------------

#------------------------------
FILE = 'news.csv'
#------------------------------
articles=[]


   



def pull_data(count = C, session=None):

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


#region get helper functions
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
#endregion
    

def web_scrapper(article_url):

    html = trafilatura.fetch_url(article_url)
    # dowload in html 
    if html is None:
        return None
    
    else:
        text = trafilatura.extract(html)
    if text:
        return text


def save_articles(rows):
    df = pd.DataFrame(rows)
    df.to_csv(FILE, index=False)
    print(f"saved article to {FILE} total of {len(rows)} articles")
    
seen_titles = set()
seen_tickers=[]

rows=[]
def main():
    
    stream = pull_data(count=C, session=None)
  
    for article in track(stream, description="CHECKING"):
 
        title = article['content']['title']
        if title in seen_titles:
            print("[yellow] duplicate skipping...[/yellow]")
            continue

        seen_titles.add(title)


        date = get_date(article=article)
        link_ = get_link(article=article)
        txt = web_scrapper(link_)
        ticker = get_ticker(article=article)


        if ticker is not None and txt is not None:

            conclusion = analyze_text(txt)
            conc_final = conclusion['conclusion']
            print(f"Conclusion {conc_final}")
            
            positive_tickers=[]
            negative_tickers=[]
            positive_sentinces=[]
            negative_sentinces=[]

            for symbol in ticker:
                sym = symbol['symbol']
                print(sym)
                seen_tickers.append(sym)

                if conclusion['conclusion'] == 'positive':
                    positive_tickers.append(sym)
                if conclusion['conclusion'] == 'negative':
                    negative_tickers.append(sym)

            summary = {"article":title, 
                    "pos_tickers":positive_tickers,
                        "neg_tickers":negative_tickers,  #this dont work
                    "conclusion":conc_final,
                    "link":link_
            }
            rows.append(summary)
            save_articles(rows)
            

         

if __name__ == "__main__":
    print(f.renderText("-"*10))
    print(f.renderText("NEWS BOT"))
    print(f.renderText("-"*10))
    print("[bold black]- Carson Shae\n\n")


    while LIVE == True:
        try:
            choice = rd.randint(a=LOWER, b=UPPER) 
            # makes a new int every time to hide common bot requests
            main()
            t.sleep(choice)

        except KeyboardInterrupt:
            print(STOPPED)
            break
                
    if LIVE == False:
        main()
        

                    


    






    

    












        



   