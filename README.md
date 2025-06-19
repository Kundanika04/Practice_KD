DATASET for REVIEW FILES 
https://www.geeksforgeeks.org/nlp/dataset-for-sentiment-analysis/

✅ Step-by-step Python Script
🔧 Prerequisites – Install Required Libraries
Run this once in your terminal:
bash
CopyEdit
pip install pandas openpyxl nltk
________________________________________
🧠 Python Script: sentiment_analysis_excel.py
python
CopyEdit
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon (first time only)
nltk.download('vader_lexicon')

# Load your Excel file (assumes 'Review' is the column name)
file_path = 'reviews.xlsx'  # Change this to your actual file
df = pd.read_excel(file_path)

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Define a function to get sentiment
def get_sentiment(text):
    if isinstance(text, str):
        score = analyzer.polarity_scores(text)['compound']
        if score >= 0.05:
            return 'Positive'
        elif score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    else:
        return 'No Text'

# Apply sentiment analysis
df['Sentiment'] = df['Review'].apply(get_sentiment)

# Save results to new Excel file
output_file = 'reviews_with_sentiment.xlsx'
df.to_excel(output_file, index=False)

print(f"Sentiment analysis completed. Results saved to '{output_file}'.")
________________________________________
📄 Sample Input (reviews.xlsx)
Review
I love this product!
Very bad experience.
It's okay, not great.
________________________________________
📄 Output (reviews_with_sentiment.xlsx)
Review	Sentiment
I love this product!	Positive
Very bad experience.	Negative
It's okay, not great.	Neutral
________________________________________
🛠️ Customize Column Name
If your review column has a different name (e.g., Comments, Feedback), change:
python
CopyEdit
df['Review']
to
python
CopyEdit
df['YourColumnName']
Sure! Below are two alternative versions of the sentiment analysis script:
________________________________________
✅ Version 1: Using TextBlob
🔧 Install Required Libraries
bash
CopyEdit
pip install pandas openpyxl textblob
Then run this once to download corpora:
bash
CopyEdit
python -m textblob.download_corpora
________________________________________
🧠 Python Script: sentiment_analysis_textblob.py
python
CopyEdit
import pandas as pd
from textblob import TextBlob

# Load Excel file
file_path = 'reviews.xlsx'  # Change this to your file path
df = pd.read_excel(file_path)

# Define sentiment function using TextBlob
def get_sentiment(text):
    if isinstance(text, str):
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.1:
            return 'Positive'
        elif polarity < -0.1:
            return 'Negative'
        else:
            return 'Neutral'
    return 'No Text'

# Apply to the 'Review' column
df['Sentiment'] = df['Review'].apply(get_sentiment)

# Save to new Excel file
df.to_excel("reviews_with_sentiment_textblob.xlsx", index=False)

print("Sentiment analysis with TextBlob complete. File saved.")
________________________________________
✅ Version 2: Using Transformers (BERT)
🔧 Install Required Libraries
bash
CopyEdit
pip install pandas openpyxl transformers torch
________________________________________
🧠 Python Script: sentiment_analysis_transformers.py
python
CopyEdit
import pandas as pd
from transformers import pipeline

# Load Excel file
file_path = 'reviews.xlsx'  # Change if needed
df = pd.read_excel(file_path)

# Load sentiment pipeline (uses pretrained BERT)
sentiment_pipeline = pipeline("sentiment-analysis")

# Function to apply model
def get_sentiment(text):
    if isinstance(text, str) and text.strip():
        result = sentiment_pipeline(text[:512])[0]  # Truncate to 512 tokens
        return result['label']
    return 'No Text'

# Apply to reviews
df['Sentiment'] = df['Review'].apply(get_sentiment)

# Save to Excel
df.to_excel("reviews_with_sentiment_bert.xlsx", index=False)

print("Sentiment analysis with transformers complete. File saved.")
________________________________________
⚖️ Which One Should You Use?
Method	Accuracy	Speed	Ideal For
VADER	⭐⭐	⚡⚡⚡	Short reviews, informal text
TextBlob	⭐⭐	⚡⚡	Simple polarity-based analysis
Transformers (BERT)	⭐⭐⭐⭐	⏳	High accuracy, longer reviews
________________________________________
Let me know if you want all three combined into a GUI or CLI tool!
You said:
Try with all three combined 
ChatGPT said:
Great! Here's a complete Python script that:
✅ Reads reviews from an Excel sheet
✅ Applies all three sentiment analysis methods – VADER, TextBlob, and Transformers (BERT)
✅ Saves the results in a new Excel file with three sentiment columns
________________________________________
⚙️ Setup – Install All Required Packages
bash
CopyEdit
pip install pandas openpyxl nltk textblob transformers torch
python -m textblob.download_corpora
________________________________________
🧠 Script: combined_sentiment_analysis.py
python
CopyEdit
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from transformers import pipeline
import nltk

# Download VADER lexicon
nltk.download('vader_lexicon')

# Load Excel file
file_path = 'reviews.xlsx'  # Change this if needed
df = pd.read_excel(file_path)

# Setup: VADER
vader_analyzer = SentimentIntensityAnalyzer()

def vader_sentiment(text):
    if isinstance(text, str):
        score = vader_analyzer.polarity_scores(text)['compound']
        if score >= 0.05:
            return 'Positive'
        elif score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    return 'No Text'

# Setup: TextBlob
def textblob_sentiment(text):
    if isinstance(text, str):
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.1:
            return 'Positive'
        elif polarity < -0.1:
            return 'Negative'
        else:
            return 'Neutral'
    return 'No Text'

# Setup: Transformers (BERT)
sentiment_pipeline = pipeline("sentiment-analysis")

def bert_sentiment(text):
    if isinstance(text, str) and text.strip():
        try:
            result = sentiment_pipeline(text[:512])[0]  # Truncate if needed
            return result['label']  # Returns 'POSITIVE' or 'NEGATIVE'
        except:
            return 'Error'
    return 'No Text'

# Apply all methods
df['VADER_Sentiment'] = df['Review'].apply(vader_sentiment)
df['TextBlob_Sentiment'] = df['Review'].apply(textblob_sentiment)
df['BERT_Sentiment'] = df['Review'].apply(bert_sentiment)

# Save results
output_file = 'combined_sentiment_analysis.xlsx'
df.to_excel(output_file, index=False)

print(f"✅ Sentiment analysis complete. Results saved to: {output_file}")
________________________________________
📄 Output Format
Review	VADER_Sentiment	TextBlob_Sentiment	BERT_Sentiment
I love this product!	Positive	Positive	POSITIVE
Very bad experience.	Negative	Negative	NEGATIVE
It was okay, not the best.	Neutral	Neutral	NEGATIVE
________________________________________
🔁 Optional Enhancements
•	Add confidence scores from each model
•	Create a “Final Sentiment” by voting across methods
•	Filter neutral reviews
•	Save output to CSV too
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from transformers import pipeline
import nltk

# STEP 1: Download VADER Lexicon (needed for VADER)
nltk.download('vader_lexicon')

# STEP 2: Read the Excel file into a DataFrame
df = pd.read_excel('reviews.xlsx')  # Ensure 'Review' column exists

# STEP 3: Set up VADER analyzer
vader_analyzer = SentimentIntensityAnalyzer()

def vader_sentiment(text):
    if isinstance(text, str):
        score = vader_analyzer.polarity_scores(text)['compound']
        if score >= 0.05:
            return 'Positive'
        elif score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    return 'No Text'

# STEP 4: Define TextBlob analyzer
def textblob_sentiment(text):
    if isinstance(text, str):
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.1:
            return 'Positive'
        elif polarity < -0.1:
            return 'Negative'
        else:
            return 'Neutral'
    return 'No Text'

# STEP 5: Load transformer model for BERT-based sentiment analysis
sentiment_pipeline = pipeline("sentiment-analysis")

def bert_sentiment(text):
    if isinstance(text, str) and text.strip():
        try:
            result = sentiment_pipeline(text[:512])[0]
            return result['label']  # Returns 'POSITIVE' or 'NEGATIVE'
        except:
            return 'Error'
    return 'No Text'

# STEP 6: Apply all three analyzers to the Review column
df['VADER_Sentiment'] = df['Review'].apply(vader_sentiment)
df['TextBlob_Sentiment'] = df['Review'].apply(textblob_sentiment)
df['BERT_Sentiment'] = df['Review'].apply(bert_sentiment)

# STEP 7: Save the result to a new Excel file
df.to_excel('combined_sentiment_analysis.xlsx', index=False)
print("✅ Sentiment analysis complete. File saved.")
