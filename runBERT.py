# pip install pandas openpyxl transformers torch
import pandas as pd
from transformers import pipeline
import re
import os

# === STEP 1: Load BERT Sentiment Classifier ===
print("🔄 Loading BERT model, please wait...")
classifier = pipeline("sentiment-analysis", device=-1)  # Force CPU
print("✅ Model loaded.")

# === STEP 2: Clean the text ===
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.strip()

# === STEP 3: Analyze sentiment ONLY if review exists ===
def get_bert_sentiment(text):
    if not isinstance(text, str) or text.strip() == "" or text.strip().lower() == "nan":
        return "No Review"
    
    truncated_text = text[:1000]
    try:
        result = classifier(truncated_text)[0]
        print(f"Processed: {truncated_text[:30]}... → {result['label']}")
        return result['label']  # 'POSITIVE' or 'NEGATIVE'
    except Exception as e:
        return f"ERROR: {str(e)}"

# === STEP 4: Load CSV ===
input_file = "C:\\Users\\kunda\\OneDrive\\Desktop\\WF proj\\yelp_review_polarity_csv\\train.csv"
output_file = "reviews_with_sentiment_bert.csv"

if not os.path.exists(input_file):
    print(f"❌ File '{input_file}' not found.")
    exit()

df = pd.read_csv(input_file)

if 'Review_Text' not in df.columns:
    print("❌ Column 'Review_Text' not found in CSV.")
    exit()

# === STEP 5: Clean and Analyze ===
df['Cleaned_Review'] = df['Review_Text'].astype(str).apply(clean_text)
print("🔄 Running sentiment analysis on valid reviews...")

# Only apply sentiment to non-empty cleaned reviews
df['Sentiment'] = df['Cleaned_Review'].apply(get_bert_sentiment)

# === STEP 6: Save Output ===
df.to_csv(output_file, index=False)
print(f"\n✅ Sentiment analysis complete! Output saved to: {output_file}")
