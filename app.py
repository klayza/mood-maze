# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime, timedelta
import json
import os
import re
from collections import Counter

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Change this in production

# Define emotion scores (higher is more positive)
EMOTION_SCORES = {
    "joy": 10,
    "love": 9.5,
    "admiration": 9,
    "gratitude": 8.5,
    "excitement": 8,
    "amusement": 7.5,
    "optimism": 7,
    "pride": 6.5,
    "relief": 6,
    "realization": 5.5,
    "approval": 5,
    "caring": 4.5,
    "surprise": 4,
    "curiosity": 3.5,
    "desire": 3,
    "confusion": 2.5,
    "nervousness": 2,
    "embarrassment": 1.5,
    "remorse": 1,
    "disapproval": 0.5,
    "grief": 0,
    "sadness": -0.5,
    "disappointment": -1,
    "annoyance": -1.5,
    "disgust": -2,
    "anger": -2.5
}

# Simple sentiment analysis function
def analyze_sentiment(text):
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    emotions_by_sentence = []
    
    # Example emotion patterns - in a real app, you'd use a proper NLP model
    emotion_patterns = {
        "joy": ["happy", "joy", "joyful", "pleased", "delighted"],
        "anger": ["angry", "fury", "outraged", "mad"],
        "sadness": ["sad", "unhappy", "depressed", "down"],
        "fear": ["afraid", "scared", "terrified", "fearful"],
        "love": ["love", "adore", "cherish"],
        "surprise": ["surprised", "shocked", "amazed"],
        "disgust": ["disgusted", "revolted", "gross"],
        "confusion": ["confused", "puzzled", "perplexed"],
        "gratitude": ["thankful", "grateful", "appreciate"],
        "admiration": ["admire", "impressed", "respect"],
        "amusement": ["amused", "entertained", "funny", "laughed"],
        "annoyance": ["annoyed", "irritated", "bothered"],
        "approval": ["approve", "agree", "good job"],
        "caring": ["care", "concerned", "worried about"],
        "curiosity": ["curious", "wonder", "interested"],
        "desire": ["want", "wish", "hope for", "desire"],
        "disappointment": ["disappointed", "letdown", "dissatisfied"],
        "disapproval": ["disapprove", "dislike", "not good"],
        "embarrassment": ["embarrassed", "humiliated", "ashamed"],
        "excitement": ["excited", "thrilled", "eager"],
        "grief": ["grief", "mourning", "devastated"],
        "nervousness": ["nervous", "anxious", "worried"],
        "optimism": ["optimistic", "hopeful", "looking forward"],
        "pride": ["proud", "accomplished", "achievement"],
        "realization": ["realized", "understood", "recognized"],
        "relief": ["relieved", "reassured", "calmed"],
        "remorse": ["remorse", "regret", "sorry"],
    }
    
    # Analyze each sentence
    for i, sentence in enumerate(sentences):
        if not sentence.strip():
            continue
            
        sentence_emotions = {}
        for emotion, keywords in emotion_patterns.items():
            sentence_lower = sentence.lower()
            count = sum(1 for keyword in keywords if keyword in sentence_lower)
            if count > 0:
                sentence_emotions[emotion] = count
        
        # Default to "neutral" if no emotions detected
        detected_emotion = max(sentence_emotions.items(), key=lambda x: x[1])[0] if sentence_emotions else "neutral"
        
        emotions_by_sentence.append({
            "text": sentence,
            "emotion": detected_emotion
        })
    
    # Get overall emotion
    all_emotions = [s["emotion"] for s in emotions_by_sentence if s["emotion"] != "neutral"]
    most_common = Counter(all_emotions).most_common(1)
    overall_emotion = most_common[0][0] if most_common else "neutral"
    
    return {
        "overall_emotion": overall_emotion,
        "sentences": emotions_by_sentence
    }

# Ensure data directory exists
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_user_data_path(user_id="default"):
    """Get path to user data file"""
    return os.path.join(DATA_DIR, f"{user_id}_entries.json")

def save_entry(entry, user_id="default"):
    """Save a journal entry to file"""
    file_path = get_user_data_path(user_id)
    
    # Load existing entries
    entries = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            entries = json.load(f)
    
    # Add new entry
    entries.append(entry)
    
    # Save updated entries
    with open(file_path, 'w') as f:
        json.dump(entries, f, indent=2)

def load_entries(user_id="default"):
    """Load all journal entries for a user"""
    file_path = get_user_data_path(user_id)
    
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if request.method == 'POST':
        text = request.form.get('entry', '')
        tags = request.form.get('tags', '').split(',')
        tags = [tag.strip() for tag in tags if tag.strip()]
        
        # Analyze sentiment
        analysis = analyze_sentiment(text)
        
        # Create entry object
        entry = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "text": text,
            "tags": tags,
            "analysis": analysis
        }
        
        # Save entry
        save_entry(entry)
        
        return redirect(url_for('timeline'))
        
    return render_template('journal.html', now=datetime.now())

@app.route('/timeline')
def timeline():
    return render_template('timeline.html')

@app.route('/api/entries')
def api_entries():
    entries = load_entries()
    return jsonify(entries)

@app.route('/api/week_data')
def api_week_data():
    year = int(request.args.get('year', datetime.now().year))
    week = int(request.args.get('week', datetime.now().isocalendar()[1]))
    
    # Calculate start and end dates for the week
    start_date = datetime.strptime(f'{year}-W{week}-1', '%Y-W%W-%w').date()
    end_date = start_date + timedelta(days=6)
    
    # Format as strings for comparison
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    
    # Get all entries
    all_entries = load_entries()
    
    # Filter entries for the specified week
    week_entries = [entry for entry in all_entries if start_str <= entry["date"] <= end_str]
    
    # Group by day
    days_data = {}
    for i in range(7):
        day_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        day_entries = [entry for entry in week_entries if entry["date"] == day_date]
        
        # Calculate dominant emotion for the day
        emotions = []
        for entry in day_entries:
            emotions.append(entry["analysis"]["overall_emotion"])
        
        most_common = Counter(emotions).most_common(1)
        dominant_emotion = most_common[0][0] if most_common else "neutral"
        emotion_score = EMOTION_SCORES.get(dominant_emotion, 0)
        
        days_data[day_date] = {
            "date": day_date,
            "emotion": dominant_emotion,
            "score": emotion_score,
            "entries": day_entries
        }
    
    return jsonify({
        "start_date": start_str,
        "end_date": end_str,
        "days": days_data
    })

if __name__ == '__main__':
    app.run(debug=True)