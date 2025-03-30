# Mood Maze

A web application that lets users write about their day, analyze their emotions, and visualize their emotional journey over time.

## Features

- **Journal Entry**: Write about your day in a clean, distraction-free environment
- **Sentiment Analysis**: AI-powered emotion detection based on journal entries
- **Timeline Visualization**: View your emotional patterns over time with an intuitive weekly bar chart

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: JSON file
- **Sentiment Analysis**: BERT-based emotion detection (using transformers library)

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```
   pip install flask torch transformers
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Open your browser and navigate to http://localhost:5000

## Project Structure

- `app.py`: Main Flask application
- `sentiment_analysis.py`: Emotion detection functionality
- `templates/`: HTML templates
- `static/css/`: CSS stylesheets
- `journal_data.json`: Data storage file (created automatically) 