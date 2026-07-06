from transformers import pipeline
from collections import Counter
import re

MODEL = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
_fin = None


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


def finBERT(sentence):
    if not isinstance(sentence, str) or not sentence.strip():
        return None

    fin = get_model()

    result = fin(sentence[:2000])

    if isinstance(result[0], list):
        result = result[0]

    scores = {}

    for item in result:
        scores[item["label"]] = item["score"] * 100

    positive = scores.get("positive", 0)
    negative = scores.get("negative", 0)

    if positive >= negative:
        label = "positive"
        score = positive
    else:
        label = "negative"
        score = negative

    output = {
        "sentence": sentence,
        "label": label,
        "score": score,
        "positive": positive,
        "negative": negative,
        "neutral": scores.get("neutral", 0),
    }
    #debug prints for model test
    #print("\nSentence:", sentence)
    #print(f"Final label: {output['label']}")
    #print(f"Positive: {output['positive']:.2f}%")
    #print(f"Negative: {output['negative']:.2f}%")
    #print(f"Neutral: {output['neutral']:.2f}%")

    return output


def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = sentences[0:5:1] #grab first 5 sentices
    return sentences


def results(outputs):
    labels = []

    for item in outputs:
        if item is not None:
            labels.append(item["label"])

    if not labels:
        return None

    label_count = Counter(labels)
    final_label = label_count.most_common(1)[0][0]

    print("Overall sentiment:", final_label)

    return final_label

high_positive=[]
high_negative=[]

def analyze_text(text):
    best_fit = []

    sentences = split_sentences(text)

    for sentence in sentences:
        output = finBERT(sentence)
        if output['positive'] >= 90:
            high_positive.append(sentence)
        if output['negative'] >= 90:
            high_negative.append(sentence)
        

        if output is not None:
            best_fit.append(output)

    conclusion = results(best_fit)
    #print(f"POSITIVE:{high_positive} NEGATIVE: {high_negative}")

    if len(high_positive) == 5:
        print("VERY HIGH POSITIVE")
    if len(high_negative) == 5:
        print("VERY HIGH NEGATIVE")
    return {
        "conclusion": conclusion,
        "sentences": best_fit
    }