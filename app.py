from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime, timedelta
import uuid
from sentiment_analysis import analyze_sentiment_using_bert

app = Flask(__name__)

DATA_FILE = 'journal_data.json'

# Emotion score mapping (higher is better)
EMOTION_SCORES = {
    'love': 3, 'joy': 3, 'happiness': 3, 'excitement': 3, 'optimism': 3, 'pride': 3, 'gratitude': 3,
    'amusement': 2, 'admiration': 2, 'approval': 2, 'caring': 2, 'curiosity': 2, 'realization': 2, 'relief': 2, 'surprise': 2,
    'neutral': 1, 'desire': 1, 'nervousness': 1, 'confusion': 1,
    'disappointment': 0, 'sadness': 0, 'grief': 0, 'fear': 0, 'remorse': 0, 'anger': 0, 'annoyance': 0, 
    'disapproval': 0, 'disgust': 0, 'embarrassment': 0
}

# Context processor for templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

def load_journal_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_journal_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_dominant_emotion(emotions_list):
    #TODO: sometimes there are emotion lists that have neutral with another non-neutral emotion, when this
    # is the case, remove the neutral. ex: ['neutral', 'happy'] -> ['happy']
    if not emotions_list:
        return "neutral"
    
    # Flatten the list of emotions from all sentences
    all_emotions = []
    for item in emotions_list:
        all_emotions.extend(item['emotions'])
    
    # Count occurrences of each emotion
    emotion_counts = {}
    for emotion in all_emotions:
        if emotion in emotion_counts:
            emotion_counts[emotion] += 1
        else:
            emotion_counts[emotion] = 1
    
    # Find the most common emotion
    if emotion_counts:
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
        return dominant_emotion
    
    return "neutral"

def get_emotion_score(emotion):
    return EMOTION_SCORES.get(emotion, 1)  # Default to 1 if emotion not found

def get_week_start_date(date_str=None):
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date = datetime.now()
    
    # Find the start of the week (Monday)
    start_of_week = date - timedelta(days=date.weekday())
    return start_of_week.strftime("%Y-%m-%d")

def get_week_data(start_date):
    data = load_journal_data()
    # Initialize the week with empty data
    week_start = datetime.strptime(start_date, "%Y-%m-%d")
    week_data = {}
   
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        week_data[day_str] = {
            "day_name": day.strftime("%a"),
            "date": day_str,
            "entries": [],  # Start with an empty list instead of None
            "dominant_emotion": None,
            "score": 0
        }
   
    # Fill in data for days that have entries
    for entry in data:
        entry_date = entry["date"]
        if entry_date in week_data:
            # Append the entry text to the entries list
            week_data[entry_date]["entries"].append(entry)
            
            # For dominant_emotion and score, you might want to:
            # 1. Use the most recent entry's values
            # 2. Or calculate an aggregate (most common emotion, average score)
            # This implementation uses the latest entry's values
            week_data[entry_date]["dominant_emotion"] = entry["dominant_emotion"]
            week_data[entry_date]["score"] = entry["score"]
   
    return list(week_data.values())

def get_all_week_start_dates():
    data = load_journal_data()
    if not data:
        return []
    
    dates = [datetime.strptime(entry["date"], "%Y-%m-%d") for entry in data]
    
    # Find unique week start dates
    week_starts = set()
    for date in dates:
        week_start = date - timedelta(days=date.weekday())
        week_starts.add(week_start.strftime("%Y-%m-%d"))
    
    return sorted(list(week_starts), reverse=True)


def get_week_number(date_str):
    """
    Calculate the ISO week number from a date string in 'YYYY-MM-DD' format.
    
    Args:
        date_str (str): Date string in 'YYYY-MM-DD' format
        
    Returns:
        int: ISO week number (1-53)
    """
    if isinstance(date_str, str):
        # Parse the date string to a datetime object
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            # Return None if date format is invalid
            return None
    elif isinstance(date_str, (datetime, date)):
        date_obj = date_str.date() if isinstance(date_str, datetime) else date_str
    else:
        # Return None for unsupported types
        return None
        
    # Calculate the ISO week number
    return date_obj.isocalendar()[1]


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if request.method == 'POST':
        text = request.form.get('journal_text', '')
        
        if text.strip():
            # Analyze sentiment
            emotions_data = analyze_sentiment_using_bert(text)
            dominant_emotion = get_dominant_emotion(emotions_data)
            score = get_emotion_score(dominant_emotion)
            
            # Save journal entry
            data = load_journal_data()
            entry = {
                "id": str(uuid.uuid4()),
                "text": text,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "emotions_data": emotions_data,
                "dominant_emotion": dominant_emotion,
                "score": score
            }
            data.append(entry)
            save_journal_data(data)
            
            # Redirect to timeline view
            return redirect(url_for('timeline'))
        
    return render_template('journal.html')

@app.route('/timeline')
@app.route('/timeline/<start_date>')
def timeline(start_date=None):
    if start_date is None:
        start_date = get_week_start_date()
    
    week_data = get_week_data(start_date)
    all_weeks = get_all_week_start_dates()
    
    # Check if there's any data
    has_entries = any(day["entries"] for day in week_data)
    
    # Find previous and next weeks
    current_week_index = all_weeks.index(start_date) if start_date in all_weeks else -1
    prev_week = all_weeks[current_week_index + 1] if current_week_index < len(all_weeks) - 1 else None
    next_week = all_weeks[current_week_index - 1] if current_week_index > 0 else None
    return render_template(
        'timeline.html', 
        week_data=week_data, 
        all_weeks=all_weeks,
        current_week=start_date,
        prev_week=prev_week,
        next_week=next_week,
        has_entries=has_entries,
    )

if __name__ == '__main__':
    app.run(debug=True) 