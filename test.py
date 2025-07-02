import streamlit as st
import pandas as pd
from llama_cpp import Llama
import os

# --- CONFIG ---
MODEL_PATH = "./Meta-Llama-3.1-8B-Instruct-Q5_K_M.gguf"
N_CTX = 2048
N_THREADS = 8
MAX_TOKENS = 256

# --- Load the model (cache to avoid reloading) ---
@st.cache_resource(show_spinner="Loading LLaMA model...")
def load_llama_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at: {MODEL_PATH}")
    return Llama(
        model_path=MODEL_PATH
    )

llm = load_llama_model()

# --- Helper functions ---
def generate_sentiment_prompt(review):
    return f"""You are a sentiment analysis assistant.
Your task is to analyze the sentiment of customer reviews and respond with ONLY ONE WORD: Positive, Neutral, or Negative.
If review sounds like a suggestion for improvement or If anything is unclear, respond with Neutral. 

Review: "{review}"
Sentiment:"""

def ask_about_data_prompt(data_summary, user_question):
    return f"""You are an intelligent assistant. The user has uploaded a dataset of customer reviews.

Here is the summary of the reviews:
{data_summary}

User Question: {user_question}
Answer:"""

def analyze_sentiment(review):
    prompt = generate_sentiment_prompt(review)
    output = llm(prompt, max_tokens=MAX_TOKENS, stop=["\n"])
    return output["choices"][0]["text"].strip()

def get_summary(df):
    summary = df['Sentiment'].value_counts().to_dict()
    result = (
        f"Positive: {summary.get('Positive', 0)}\n"
        f"Neutral: {summary.get('Neutral', 0)}\n"
        f"Negative: {summary.get('Negative', 0)}"
    )
    return result

# --- Streamlit UI ---
st.title("📊 Excel Review Sentiment Analyzer (LLaMA 3.1 GGUF)")
uploaded_file = st.file_uploader("Upload an Excel file with a 'Review' column", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    if "Review" not in df.columns:
        st.error("The uploaded Excel file must contain a column named 'Review'.")
    else:
        st.success("File uploaded successfully!")
        st.write("Preview of your data:", df.head())

        if st.button("Run Sentiment Analysis"):
            with st.spinner("Analyzing sentiment..."):
                df["Sentiment"] = df["Review"].apply(
                    lambda r: analyze_sentiment(str(r)) if pd.notna(r) else "N/A"
                )
                summary_text = get_summary(df)
                st.write("### Sentiment Summary", summary_text)
                st.write("### Annotated Data", df)

        # Ask questions about the data
        st.markdown("---")
        st.subheader("💬 Ask Questions About the Reviews")

        user_question = st.text_input("Enter your question:")
        if user_question and "Sentiment" in df.columns:
            with st.spinner("Thinking..."):
                summary = get_summary(df)
                prompt = ask_about_data_prompt(summary, user_question)
                response = llm(prompt, max_tokens=MAX_TOKENS, stop=["\n"])
                st.write("🧠 Response:", response["choices"][0]["text"].strip())
