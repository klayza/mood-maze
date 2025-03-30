import re
import torch
from transformers import BertTokenizer, BertForSequenceClassification

model_name = "bhadresh-savani/bert-base-uncased-emotion"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Multi-label GoEmotions emotion classes
emotion_labels = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion",
    "curiosity", "desire", "disappointment", "disapproval", "disgust", "embarrassment",
    "excitement", "fear", "gratitude", "grief", "joy", "love", "nervousness", "optimism",
    "pride", "realization", "relief", "remorse", "sadness", "surprise", "neutral"
]

def analyze_sentiment_using_bert(text, threshold=0.3):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    emotions_by_sentence = []

    for sentence in sentences:
        if not sentence.strip():
            continue

        inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Apply sigmoid to get probabilities
        probs = torch.sigmoid(outputs.logits)[0]

        # Get labels above threshold
        top_emotions = [emotion_labels[i] for i, p in enumerate(probs) if p > threshold]

        emotions_by_sentence.append({
            "text": sentence,
            "emotions": top_emotions if top_emotions else ["neutral"]
        })

    return emotions_by_sentence
