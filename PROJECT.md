## Project Description. Mood Maze. This web app lets users write about their day and add tags to their entry. 

### Journal page
The journal page is a minimal, and clean page that lets the user write about their day. It is a textarea that takes up the entire page width (but with responsive padding). The font is 18px. At the bottom of the page to the right is a submit button that will light up when there the textarea is no empty.

### Sentiment Analysis / submit
After their journal is entered it will go through a sentiment analysis (which is already created, just import this: from sentiment_analysis import analyze_sentiment_using_bert. The function inputs a paragraph and outputs something like this example: [{'text': 'I got a raise!', 'emotions': ['excitement', 'joy']}, {'text': 'I am now at a loss for words', 'emotions': ['disappointment', 'sadness']}]


### Timeline page
Once their entry is submitted it will redirect the user to the timeline page of the current week. The timeline page will show a clean, and minimal view of previous entries. It is a bar chart of each day of the week, with the score relating to dominant emotion of the day. Also, please assign each emotion with a score with love, joy, and happiness being the highest, and sadness, grief, and fear being the lowest score (out of 3 points). The day's bar is labeled with it's dominant emotion and day of the week. The day of the week is shown at the bottom, and it's dominant emotion at the top. At the top of the page is the dropdown to select other weeks, but only if there is data for other weeks. If there is no user data at all, then prompt the user to create an entry. If there are no entries for the current week, then prompt them to create an entry. Next to the dropdown are left and right arrows to switch to other weeks.


### Home page
A unique, and fun, crafty, landing page for the app.


## UI
The UI is clean, modern, and user-friendly.


## Tech stack
Use Python Flask for API. json for simple db.



Here are all the possible emotions:
```emotions.txt
admiration
  
amusement
  
anger
  
annoyance
  
approval
  
caring
  
confusion
  
curiosity
  
desire
  
disappointment
  
disapproval
  
disgust
  
embarrassment
  
excitement
  
fear
  
gratitude
  
grief
  
joy
  
love
  
nervousness
  
optimism
  
pride
  
realization
  
relief
  
remorse
  
sadness
  
surprise
\```

flask==2.2.3
torch==2.0.1
transformers==4.30.2