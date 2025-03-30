import torch
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load GoEmotions model and tokenizer
model_name = "SamLowe/roberta-base-go_emotions"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Extract emotion labels
emotion_labels = list(model.config.id2label.values())

def analyze_sentiment_using_bert(text, threshold=0.3):
    """
    Analyzes the input journal text and returns:
    - a list of emotions per sentence (just emotion names)
    - to be used by the existing get_dominant_emotion logic in app.py
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    results = []

    for sentence in sentences:
        if not sentence.strip():
            continue

        inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            logits = model(**inputs).logits
        probs = torch.sigmoid(logits)[0]

        detected_emotions = [
            emotion_labels[i]
            for i in range(len(probs)) if probs[i] >= threshold
        ]

        # Fallback to "neutral" if no emotion passes threshold
        if not detected_emotions:
            detected_emotions = ["neutral"]

        results.append({
            "sentence": sentence,
            "emotions": detected_emotions
        })

    return results


if __name__ == "__main__":
    print(analyze_sentiment_using_bert("Today is stressful, I can't get the code to work. What should I do? Nothing is working."))
    