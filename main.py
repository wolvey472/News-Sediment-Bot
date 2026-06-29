#Web scraping
import requests as rq
import feedparser
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

if tf.__version__:
    print("woprks")
else:
    print("NOT WORKING")