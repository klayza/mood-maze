import re
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load model and tokenizer for emotion detection
model_name = "bhadresh-savani/bert-base-uncased-emotion"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Emotion labels (GoEmotions dataset)
emotion_labels = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion",
    "curiosity", "desire", "disappointment", "disapproval", "disgust", "embarrassment",
    "excitement", "fear", "gratitude", "grief", "joy", "love", "nervousness", "optimism",
    "pride", "realization", "relief", "remorse", "sadness", "surprise", "neutral"
]

def analyze_sentiment_using_bert(text):
    # Split the input text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    emotions_by_sentence = []

    # Analyze each sentence using the BERT model
    for sentence in sentences:
        if not sentence.strip():
            continue
            
        # Tokenize input sentence
        inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)
        
        # Predict emotion using BERT model
        with torch.no_grad():
            outputs = model(**inputs)

        # Get the predicted label for emotion
        predicted_label = torch.argmax(outputs.logits, dim=1).item()
        detected_emotion = emotion_labels[predicted_label]

        # Append the result to the list
        emotions_by_sentence.append({
            "text": sentence,
            "emotion": detected_emotion
        })
    
    return emotions_by_sentence