# Real-Time Financial News Sentiment Bot

A Python bot that detects newly published financial news, extracts the article text, and uses FinBERT to classify the sentiment as **positive**, **negative**, or **neutral**.

## Overview

Financial markets can react quickly to breaking news. This project is designed to find new articles, analyze them almost immediately, and produce a sentiment result that could eventually be used in a trading alert or market-monitoring system.

## Features

- Detects newly published financial articles
- Web scrapes and extracts article text
- Analyzes financial language using FinBERT
- Classifies sentiment as positive, negative, or neutral
- Avoids repeatedly processing the same articles
- Produces results quickly for real-time monitoring

## How It Works

1. The bot checks a financial news source for new articles.
2. It compares the articles against those it has already processed.
3. It extracts and cleans the text from each new article.
4. The text is passed into the FinBERT model.
5. The bot returns the predicted sentiment and confidence score.

## Technologies Used

- Python
- FinBERT
- Hugging Face Transformers
- PyTorch
- Requests
- Beautiful Soup
- Pandas

## Project Structure

financial-news-sentiment-bot/
├── main.py
├── scraper.py
├── sentiment.py
├── requirements.txt
├── .gitignore
└── README.md
