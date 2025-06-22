# pip install pandas openpyxl textblob nltk
# python -m textblob.download_corpora
import pandas as pd
from textblob import TextBlob
import re
import nltk
from nltk.corpus import stopwords

# Download stopwords for the first time
nltk.download('stopwords')

# Define stopwords
stop_words = set(stopwords.words('english'))

# Function to clean review text
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()                                # Lowercase
    text = re.sub(r'[^a-zA-Z\s]', '', text)            # Remove special chars
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

# Function to get sentiment from TextBlob
def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

# === Step 1: Load Excel file ===
input_file = "C:\\Users\\kunda\\OneDrive\\Desktop\\WF proj\\yelp_review_polarity_csv\\train.csv"           # Change to your input file
output_file = "reviews_with_sentiment.xlsx"

try:
    df = pd.read_csv(input_file)
except FileNotFoundError:
    print(f"File '{input_file}' not found.")
    exit()

# === Step 2: Ensure required column exists ===
if 'Review_Text' not in df.columns:
    print("Error: 'Review_Text' column not found in Excel.")
    exit()

# === Step 3: Clean text ===
df['Cleaned_Review'] = df['Review_Text'].astype(str).apply(clean_text)

# === Step 4: Sentiment Analysis ===
df['Sentiment'] = df['Cleaned_Review'].apply(get_sentiment)

# === Step 5: Save to new Excel file ===
df.to_csv(output_file, index=False)
print(f"\n✅ Sentiment analysis complete! Output saved to '{output_file}'")
