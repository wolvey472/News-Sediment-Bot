from transformers import pipeline
import re
MODEL = "ProsusAI/finbert"

_fin = None


text = """Republic Services, Inc. (NYSE:RSG) is one of the 10 Best Stocks to Buy According to Billionaire Richard Chilton.
Republic Services, Inc. (NYSE:RSG) is one of the largest waste collection companies in America. Its shares are down by 11.5% over the past year and are up by 3% year-to-date. Citi discussed the firm on May 12th as it cut the share price target to $247 from $253 and kept a Buy rating on the shares. Similarly, CIBC also reduced the share price target. It lowered it to $249 from $251 and kept an Outperform rating on the stock. The financial firm discussed Republic Services, Inc. (NYSE:RSG)'s first-quarter earnings and remarked that despite macroeconomic struggles, the results were solid. As part of its earnings, the waste collection firm posted $4.11 billion in revenue and $1.70 in earnings per share to beat analyst estimates of $4.10 billion and $1.64.
Republic Services, Inc. (NYSE:RSG)'s shares are trading at a forward P/E ratio of 29.67, which is higher than the S&P's 21. The firm scored a win earlier this month after the Federal Trade Commission allowed it to acquire assets from TD*X Associates. The latter operates facilities to process hazardous waste.
While we acknowledge the potential of RSG as an investment, we believe certain AI stocks offer greater upside potential and carry less downside risk. If you're looking for an extremely undervalued AI stock that also stands to benefit significantly from Trump-era tariffs and the onshoring trend, see our free report on the best short-term AI stock.
READ NEXT: 33 Stocks That Should Double in 3 Years and Cathie Wood 2026 Portfolio: 10 Best Stocks to Buy.
Disclosure: None. Follow Insider Monkey on Google News."""


def split_sentences(text):
    if not isinstance(text, str):
        return []

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    return [s.strip() for s in sentences if s.strip()]

def chunks_of_3(text):
    sentences = split_sentences(text)

    chunks = []

    for i in range(0, len(sentences), 3):
        chunk = " ".join(sentences[i:i + 3])
        chunks.append(chunk)

    return chunks

def get_model():
    global _fin

    if _fin is None:
        print("Loading FinBERT...")
        _fin = pipeline(
            "text-classification",
            model=MODEL,
            tokenizer=MODEL,
            top_k=None
        )
        print("Model loaded")

    return _fin


def finBERT(t):
    if not isinstance(t, str) or not t.strip():
        return {
            "label": None,
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }

    fin = get_model()

    result = fin(t[:2000])

    # Handles both possible result shapes:
    # [[{'label': ..., 'score': ...}, ...]]
    # [{'label': ..., 'score': ...}, ...]
    if isinstance(result[0], list):
        result = result[0]

    scores = {
        "positive": 0,
        "negative": 0,
        "neutral": 0
    }

    for item in result:
        label = item["label"].lower()
        score = item["score"]
        scores[label] = score

    positive = scores["positive"] * 100
    negative = scores["negative"] * 100
    neutral = scores["neutral"] * 100

    final_label = max(scores, key=scores.get).upper()

    print(f"Final label: {final_label}")
    print(f"Positive: {positive:.2f}%")
    print(f"Negative: {negative:.2f}%")
    print(f"Neutral: {neutral:.2f}%")

    return {
        "label": final_label,
        "positive": positive,
        "negative": negative,
        "neutral": neutral
    }


def finBERT_raw(t):
    fin = get_model()
    result = fin(t[:2000])
    return result


if __name__ == "__main__":
    text = text

    result = finBERT(text)

    positive = result["positive"]
    negative = result["negative"]
    neutral = result["neutral"]
    label = result["label"]

    print(result)

    text_chunks = chunks_of_3(text)

    for chunk in text_chunks:
        result = finBERT(chunk)

        print("TEXT:")
        print(chunk)

        print("RESULT:")
        print(result)

        print("-" * 50)