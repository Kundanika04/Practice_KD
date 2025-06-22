# pip install pandas openpyxl nltk
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re
from nltk.corpus import stopwords

# Download necessary resources
nltk.download('vader_lexicon')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

# Clean review text
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = [word for word in text.split() if word not in stop_words]
    return " ".join(words)

# Get sentiment using VADER
sia = SentimentIntensityAnalyzer()

def get_vader_sentiment(text):
    score = sia.polarity_scores(text)
    compound = score['compound']
    if compound >= 0.1:
        return 'Positive'
    elif compound <= -0.1:
        return 'Negative'
    else:
        return 'Neutral'

# Load Excel
input_file = "C:\\Users\\kunda\\OneDrive\\Desktop\\WF proj\\yelp_review_polarity_csv\\train.csv" 
output_file = "reviews_with_sentiment_vader.xlsx"
df = pd.read_csv(input_file)

if 'Review_Text' not in df.columns:
    print("Missing 'Review_Text' column.")
    exit()

df['Cleaned_Review'] = df['Review_Text'].astype(str).apply(clean_text)
df['Sentiment'] = df['Cleaned_Review'].apply(get_vader_sentiment)

df.to_csv(output_file, index=False)
print(f"\n✅ VADER Sentiment Analysis complete. Saved to: {output_file}")

