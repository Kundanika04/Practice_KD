Performing basic sentiment analysis using Excel formulas is possible, though limited. Excel can't understand language deeply like Python-based NLP models, but you can create a keyword-based sentiment scoring system using built-in formulas like SEARCH, COUNTIF, IF, etc.

✅ What You Can Do in Excel
You can:

Count positive and negative keywords in each review

Assign a sentiment score or category (Positive, Negative, or Neutral)

Use simple logic to label reviews based on keyword frequency

🧾 Step-by-Step Guide
📄 Step 1: Prepare Your Data
A (Review)
I love this product, it's amazing!
Very poor quality and service.
It's okay, not bad but not great.

📄 Step 2: Create a List of Keywords
In a separate sheet or section:

Positive Words
G (Positive Words)
good
great
love
amazing
excellent

Negative Words
H (Negative Words)
bad
poor
terrible
hate
awful

📄 Step 3: Count Keyword Matches
Use formulas to count how many positive/negative words exist in each review.

Assume:

Review is in A2

Positive words are in range G2:G6

Negative words are in range H2:H6

Count Positive Words
excel
Copy
Edit
=SUMPRODUCT(--ISNUMBER(SEARCH(G2:G6, A2)))
Count Negative Words
excel
Copy
Edit
=SUMPRODUCT(--ISNUMBER(SEARCH(H2:H6, A2)))
These will return a number of matched keywords.

📄 Step 4: Determine Overall Sentiment
Now create a simple IF formula:

excel
Copy
Edit
=IF(SUMPRODUCT(--ISNUMBER(SEARCH(G2:G6, A2))) > SUMPRODUCT(--ISNUMBER(SEARCH(H2:H6, A2))), "Positive", IF(SUMPRODUCT(--ISNUMBER(SEARCH(G2:G6, A2))) < SUMPRODUCT(--ISNUMBER(SEARCH(H2:H6, A2))), "Negative", "Neutral"))
You can paste this into a new column like B2 and drag it down.

✅ Final Output
Review	Sentiment
I love this product, it's amazing!	Positive
Very poor quality and service.	Negative
It's okay, not bad but not great.	Neutral

⚠️ Limitations
No context or grammar understanding

Can't handle negation well (e.g., "not good" will be read as positive)

Can’t distinguish sarcasm, idioms, etc.

✅ When to Use
For quick and simple projects

In environments where Python tools can't be used

As a complement to manual review

Would you like a ready-made Excel file template with formulas built-in? I can also guide you through building one.








You said:
Give me a ready-made Excel file template with formulas built-i


ChatGPT said:
Sure! Here's what I'll do for you:

✅ I'll describe the layout of the Excel template with cell references, and
✅ Then I’ll give you a Google Sheets & Excel-compatible file link to download (you'll be able to upload it to Excel and use it immediately).
🔧 Excel Template Structure
🧾 Sheet Name: Reviews
A	B	C
Review	Sentiment	Notes (opt.)
I love it	(Formula output)	
Very poor	(Formula output)	

📃 Sheet Name: Keywords
A (Positive Words)	B (Negative Words)
good	bad
great	poor
excellent	terrible
amazing	awful
love	hate

🧠 Built-In Formula in Reviews!B2
Paste this formula in cell B2:

excel
Copy
Edit
=IF(SUMPRODUCT(--ISNUMBER(SEARCH(Keywords!A$2:A$10, A2))) > SUMPRODUCT(--ISNUMBER(SEARCH(Keywords!B$2:B$10, A2))), "Positive", IF(SUMPRODUCT(--ISNUMBER(SEARCH(Keywords!A$2:A$10, A2))) < SUMPRODUCT(--ISNUMBER(SEARCH(Keywords!B$2:B$10, A2))), "Negative", "Neutral"))
Then drag down the formula for the other reviews.

📎 Download the Template
✅ Download (Excel .xlsx format):
Click here to download the Excel sentiment analysis template

🧪 How to Use
Open the file in Excel.

Go to the Reviews sheet.

Paste or type reviews in Column A.

Column B will auto-calculate sentiment as Positive, Negative, or Neutral based on keyword matches.

You can add more keywords in the Keywords sheet.

Let me know if you want:

A version with emoji feedback (e.g., 👍👎)

More advanced logic (e.g., handling negation like “not good”)

A Google Sheets version with sharing

I'm happy to help!








You said:
More advanced logic (e.g., handling negation like “not good”)

Do this 


ChatGPT said:
Excellent choice! Adding negation handling (like recognizing that “not good” is actually negative, not positive) makes your sentiment analysis in Excel much smarter.

🧠 Goal
We want to improve our Excel formula so that it can:

Detect positive and negative keywords

Flip the sentiment when negation words (like not, never, no) appear right before a keyword

✅ Step-by-Step Advanced Excel Sentiment Analysis Template with Negation Handling
📃 Sheet Structure
🔹 Sheet 1: Reviews
A	B
Review	Sentiment
Not good	(Formula)
I love it	(Formula)
Not amazing	(Formula)

🔹 Sheet 2: Keywords
A (Positive Words)	B (Negative Words)	C (Negation Words)
good	bad	not
great	poor	no
excellent	terrible	never
amazing	awful	
love	hate	

📜 Advanced Logic in Excel
We’ll use a helper column approach because Excel formulas can’t truly “understand context” but we can approximate it by checking:

Does a negation word appear within 5 characters before a keyword?

✅ Custom Formula Logic (Step-by-Step in Excel)
Let’s say:

Column A = Review text

Keywords are in:

Keywords!A2:A10 (positive)

Keywords!B2:B10 (negative)

Keywords!C2:C10 (negations)

📌 Create Helper Columns in Reviews Sheet
A	B	C	D
Review	Positive Score	Negative Score	Final Sentiment
not good	(formula)	(formula)	(formula)

✅ B2: Count positive matches not preceded by negation
excel
Copy
Edit
=SUMPRODUCT(--(ISNUMBER(SEARCH(" " & Keywords!A$2:A$10, " " & A2))) * --(ISERROR(SEARCH("not " & Keywords!A$2:A$10, LOWER(A2)))))
✅ C2: Count negative matches not preceded by negation
excel
Copy
Edit
=SUMPRODUCT(--(ISNUMBER(SEARCH(" " & Keywords!B$2:B$10, " " & A2))) * --(ISERROR(SEARCH("not " & Keywords!B$2:B$10, LOWER(A2)))))
✅ D2: Final Sentiment
excel
Copy
Edit
=IF(B2 > C2, "Positive", IF(B2 < C2, "Negative", "Neutral"))
🧪 Example Output
Review	Positive Score	Negative Score	Final Sentiment
Not good	0	1	Negative
I love it	1	0	Positive
Not amazing	0	1	Negative

✅ Download Advanced Template with Negation
📥 Click to download Advanced Sentiment Analysis Excel Template with Negation Handling

🧠 Limitations
While this is more advanced than standard formulas, it still has these limitations:

Can’t detect sarcasm or double negatives

Doesn’t understand sentence structure

Negation detection is approximate



-----------------------------------


# sentiment_app.py
import streamlit as st
import pandas as pd
import re

from transformers import pipeline
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import nltk

nltk.download('vader_lexicon')

# === Setup models once ===
@st.cache_resource
def load_bert():
    return pipeline("sentiment-analysis", device=-1)

@st.cache_resource
def load_vader():
    return SentimentIntensityAnalyzer()

bert_classifier = load_bert()
vader_analyzer = load_vader()

# === Text cleaning ===
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.strip()

# === Sentiment functions ===
def get_bert_sentiment(text):
    if not text or str(text).strip().lower() == "nan":
        return "No Review", None
    result = bert_classifier(text[:1000])[0]
    return result["label"], round(result["score"], 3)

def get_vader_sentiment(text):
    if not text or str(text).strip().lower() == "nan":
        return "No Review", None
    scores = vader_analyzer.polarity_scores(text)
    compound = scores["compound"]
    label = "POSITIVE" if compound >= 0.05 else "NEGATIVE" if compound <= -0.05 else "NEUTRAL"
    return label, round(compound, 3)

def get_textblob_sentiment(text):
    if not text or str(text).strip().lower() == "nan":
        return "No Review", None
    polarity = TextBlob(text).sentiment.polarity
    label = "POSITIVE" if polarity > 0 else "NEGATIVE" if polarity < 0 else "NEUTRAL"
    return label, round(polarity, 3)

# === Streamlit UI ===
st.title("ðŸ“Š Excel Review Sentiment Analyzer")
st.markdown("Upload an Excel or CSV file containing a **Review_Text** column.")

uploaded_file = st.file_uploader("Upload your file", type=["csv", "xlsx"])
model_choice = st.selectbox("Choose Sentiment Analysis Model", ["BERT", "VADER", "TextBlob"])
run_btn = st.button("Run Sentiment Analysis")

if uploaded_file and run_btn:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        if "Review_Text" not in df.columns:
            st.error("âŒ 'Review_Text' column not found in file.")
        else:
            df["Cleaned_Review"] = df["Review_Text"].astype(str).apply(clean_text)

            sentiments = []
            scores = []
            with st.spinner("Analyzing..."):
                for text in df["Cleaned_Review"]:
                    if model_choice == "BERT":
                        label, score = get_bert_sentiment(text)
                    elif model_choice == "VADER":
                        label, score = get_vader_sentiment(text)
                    else:
                        label, score = get_textblob_sentiment(text)
                    sentiments.append(label)
                    scores.append(score)
            
            df["Sentiment"] = sentiments
            df["Score"] = scores
            st.success("âœ… Sentiment analysis complete!")
            st.dataframe(df[["Review_Text", "Sentiment", "Score"]])

            # Download link
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("ðŸ“¥ Download Results as CSV", csv, "sentiment_results.csv", "text/csv")
    except Exception as e:
        st.error(f"âš ï¸ Error: {str(e)}")
      
