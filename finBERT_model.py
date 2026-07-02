from transformers import pipeline
import re
MODEL = "ProsusAI/finbert"

_fin = None


text = r""" Adobe earlier reported a 13% increase in its revenue for the second quarter of its fiscal year 2026 at $6.62 billion from the $5.87 billion registered in the same period last year. The company also reported a GAAP net income during the period amounting to $1.71 billion, while non-GAAP net income registered at $2.40 billion."""

def split():
    ...


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
            "score": 0,
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
    
    scores={}


    for item in result:
        scores[item["label"]] = item["score"] * 100

    best = max(result, key=lambda x: x["score"])

    label = best["label"]
    score = best["score"] * 100

    print(f"Final label: {label}")
    print(f"Positive: {scores.get('positive', 0):.2f}%")
    print(f"Negative: {scores.get('negative', 0):.2f}%")
    print(f"Neutral: {scores.get('neutral', 0):.2f}%")

    return {
        "label": label,
        "score": score,
        "positive": scores.get("positive", 0),
        "negative": scores.get("negative", 0),
        "neutral": scores.get("neutral", 0)
    }


def finBERT_raw(t):
    fin = get_model()
    result = fin(t[:2000])
    return result


if __name__ == "__main__":
    finBERT(text)