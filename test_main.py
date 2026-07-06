from project import web_scrapper, get_link, pull_data
# import only 3 major functions
# other get_ functions are simply for data
import pytest
from finBERT_model import analyze_text

#------
#    pytest test_project.py
#------

url = ["https://finance.yahoo.com/markets/article/micron-stock-has-now-plunged-to-a-surprising-level-141142114.html",
       "https://finance.yahoo.com/technology/article/microsoft-to-cut-3200-jobs-amid-xbox-restructuring-our-business--is-not-healthy-145525525.html",
    ]

bad_url = "https://www.nytimes.com/2026/07/06/world/middleeast/nato-summit-turkey-erdogan-trump.html"
# cant webscrape NYT 
def fake_json():
    return {
        "content": {
            "title": "Apple Stock Rises After Strong Earnings",
            "pubDate": "2026-07-05T23:30:00+00:00",
            "canonicalUrl": {
                "url": "https://example.com/apple-news"
            },
            "finance": {
                "stockTickers": [
                    {"symbol": "AAPL"},
                    {"symbol": "MSFT"}
                ]
            }
        }
    }


def test_web_scrapper():
    for each in url:
        text = web_scrapper(each)

        assert isinstance(text, str) 
    #simpily test if the url return a str when webscraped

    text = web_scrapper(bad_url)

    assert text is None
    # kinda random but show you cant scrape NYT and returns None

def test_get_link():
        

    link = get_link(fake_json())
    assert link == "https://example.com/apple-news"

def test_pull_data():
    '''
    200 -> good response
    '''
    fake_stream = [
    fake_json(),
    fake_json()
]
    class FakeResponse:
        status_code = 200
        url = "https://example.com" 
        #dont want to mess with real urls
        text = "OK"

        def json(self):
            return {
                "data": {
                    "tickerStream": {
                        "stream": fake_stream
                    }
                }
            }
    class FakeSession:
        def post(self, url, json, timeout, headers):
            return FakeResponse()
        
    result = pull_data(count=2, session=FakeSession())
    # pass in a fake session to see if the data pulled = data created

    assert result == fake_stream

def test_pull_data_bad():
    '''
    400 ERR
    '''
    class FakeResponse:
        status_code = 400
        url = "https://example.com"
        text = "Bad Request"

    class FakeSession:
        def post(self, url, json, timeout, headers):
            return FakeResponse()

    result = pull_data(count=2, session=FakeSession())

    assert result == []

txt = """US stocks mostly drifted higher on Monday as pressure on the tech sector eased and oil prices rose slightly.  The tech-heavy Nasdaq Composite (^IXIC) jumped 1.1%, while the S&P 500 (^GSPC) put on 0.6%. The Dow Jones Industrial Average (^DJI) dipped below the flat line on the heels of a record-setting, holiday-shortened week for the blue-chip benchmark. Tech stocks are helping to drive gains, hinting at a return of faith in the artificial intelligence trade after the late-June slump in chip stocks. On Sunday, Nvidia (NVDA) supplier Hon Hai (2317.TW, HNHAF), also known as Foxconn, reported a stronger-than-expected rise in quarterly sales, a sign of sustained AI demand.  That has put the spotlight on quarterly results from Samsung Electronics (005930.KS, SSNLF), due on Tuesday. The world's biggest maker of memory chips is expected to post an 18-fold jump in profit year-on-year, far outstripping its total for all of 2025."""

def test_finBERT_model():
    '''
    just input text and 
    get conclusion from sentinces
    '''
    conclusion = analyze_text(text=txt)
    
    assert conclusion['conclusion'] == 'positive'

