import torch
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "SamLowe/roberta-base-go_emotions"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name) 

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

        # Apply sigmoid to logits
        probs = torch.sigmoid(outputs.logits)[0]

        # Select all labels above threshold
        detected_emotions = [
            emotion_labels[i] for i, prob in enumerate(probs) if prob >= threshold
        ]

        emotions_by_sentence.append({
            "text": sentence,
            "emotions": detected_emotions if detected_emotions else ["neutral"]
        })


    return emotions_by_sentence


if __name__ == "__main__":
    print(analyze_sentiment_using_bert("Today is stressful, I can't get the code to work. What should I do? Nothing is working."))
    