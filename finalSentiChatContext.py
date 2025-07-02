import streamlit as st
import pandas as pd
from llama_cpp import Llama
import os

# === Configuration ===
MODEL_PATH = "./Meta-Llama-3.1-8B-Instruct-Q5_K_M.gguf"
N_CTX = 2048
N_THREADS = 8
MAX_TOKENS = 256

# === Load LLaMA model with caching ===
@st.cache_resource(show_spinner="Loading LLaMA model...")
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at: {MODEL_PATH}")
    return Llama(
        model_path=MODEL_PATH,
        n_ctx=N_CTX,
        n_threads=N_THREADS
    )

llm = load_model()

# === Streamlit App Layout ===
st.set_page_config(page_title="Sentiment Chat Assistant", layout="wide")
st.title("💬 Sentiment Chat Assistant with Memory (LLaMA 3.1)")

# === File Upload ===
uploaded_file = st.file_uploader("Upload an Excel file with a 'Review' column", type=["xlsx"])

# === Session State for Memory ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "df" not in st.session_state:
    st.session_state.df = None
if "sentiment_summary" not in st.session_state:
    st.session_state.sentiment_summary = ""

# === Load and Analyze Excel File ===
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if "Review" not in df.columns:
        st.error("The uploaded Excel file must contain a column named 'Review'.")
    else:
        st.success("Excel file loaded!")
        st.session_state.df = df

        if "Sentiment" not in df.columns:
            with st.spinner("Analyzing sentiments..."):
                def generate_sentiment_prompt(review):
                    return f"""You are a sentiment classifier.
Classify this review as Positive, Neutral, or Negative.
Review: "{review}"
Sentiment (only one word):"""

                def analyze_sentiment(review):
                    prompt = generate_sentiment_prompt(str(review))
                    output = llm(prompt, max_tokens=10, stop=["\n"])
                    raw = output["choices"][0]["text"].strip().capitalize()
                    if raw.startswith("Positive"):
                        return "Positive"
                    elif raw.startswith("Negative"):
                        return "Negative"
                    elif raw.startswith("Neutral"):
                        return "Neutral"
                    return "Unrecognized"

                df["Sentiment"] = df["Review"].apply(
                    lambda r: analyze_sentiment(r) if pd.notna(r) else "N/A"
                )
                st.session_state.df = df

        summary_counts = st.session_state.df["Sentiment"].value_counts().to_dict()
        summary = (
            f"Positive: {summary_counts.get('Positive', 0)}\n"
            f"Neutral: {summary_counts.get('Neutral', 0)}\n"
            f"Negative: {summary_counts.get('Negative', 0)}"
        )
        st.session_state.sentiment_summary = summary
        st.write("### Summary of Sentiment:")
        st.text(summary)

# === Chat Interface ===
st.markdown("---")
st.subheader("💬 Ask Anything About the Reviews")

# Chat input box
user_input = st.chat_input("Ask a question about the data (e.g., 'How many negative reviews?')")

if user_input:
    # Append user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Detect if user input is review-related
    file_keywords = [
        "review", "reviews", "sentiment", "positive", "negative",
        "neutral", "satisfied", "customer", "summary", "file", "data"
    ]
    is_file_related = any(kw in user_input.lower() for kw in file_keywords)

    # If asking about file but no file is uploaded
    if is_file_related and (st.session_state.df is None or st.session_state.sentiment_summary == ""):
        reply = "⚠️ There's no file to analyze. Please upload an Excel file with reviews."
    else:
        # === Full context + chat memory ===
        system_context = f"""You are an intelligent assistant. When a user uploads a file of customer reviews,
you perform sentiment analysis, and answer questions about the results.

Here is the summary of the uploaded file:
{st.session_state.sentiment_summary if st.session_state.sentiment_summary else '[No file uploaded]'}

You should use this summary to answer user questions when relevant.
Otherwise, respond as a general assistant.
"""

        # Build conversation history prompt
        conversation = f"{system_context}\n\n"
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                conversation += f"User: {message['content']}\n"
            else:
                conversation += f"Assistant: {message['content']}\n"
        conversation += "Assistant:"

        # Generate response from model
        with st.spinner("Generating response..."):
            output = llm(conversation, max_tokens=MAX_TOKENS, stop=["\nUser:", "\nAssistant:"])
            reply = output["choices"][0]["text"].strip()

    # Append model reply
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

# Display chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
