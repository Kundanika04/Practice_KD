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
        model_path=MODEL_PATH
    )

llm = load_model()

# === Streamlit App Layout ===
st.set_page_config(page_title="Sentiment Chat Assistant", layout="wide")
st.title("💬 Sentiment Chat Assistant with Memory (LLaMA 3.1)")

# === File Upload ===
uploaded_file = st.file_uploader("Upload an Excel file with a 'Review' column", type=["xlsx"])

# Session State for Conversation Memory
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

# Handle input and update chat history
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # If no file uploaded or sentiment summary unavailable
    if st.session_state.df is None or st.session_state.sentiment_summary == "":
        reply = "⚠️ There's no file to analyze. Please upload an Excel file with reviews."
    else:
        # Construct system prompt with summary
        system_context = f"""You are an AI assistant analyzing customer reviews from an Excel file.
The reviews have been classified into sentiment categories: Positive, Neutral, and Negative.

Here is the summary:
{st.session_state.sentiment_summary}

Use this to answer questions asked by the user."""

        # Create conversation string
        conversation = f"{system_context}\n\n"
        for message in st.session_state.chat_history:
            role = message["role"]
            content = message["content"]
            if role == "user":
                conversation += f"User: {content}\n"
            else:
                conversation += f"Assistant: {content}\n"
        conversation += "Assistant:"

        # Generate response
        with st.spinner("Generating response..."):
            output = llm(conversation, max_tokens=MAX_TOKENS, stop=["\nUser:", "\nAssistant:"])
            reply = output["choices"][0]["text"].strip()

    # Append assistant's reply
    st.session_state.chat_history.append({"role": "assistant", "content": reply})


# Display Chat History
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])
