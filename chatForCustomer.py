import streamlit as st
import pandas as pd
from llama_cpp import Llama
import os
import re

# === Configuration ===
MODEL_PATH = "./Meta-Llama-3.1-8B-Instruct-Q5_K_M.gguf"
N_CTX = 4096  # Increased context size for more data
N_THREADS = 8
MAX_TOKENS_RESPONSE = 512 # Increased for more detailed answers

# === Load LLaMA model with caching ===
@st.cache_resource(show_spinner="Loading LLaMA model...")
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"Model not found at: {MODEL_PATH}")
        st.stop()
    return Llama(
        model_path=MODEL_PATH,
        n_ctx=N_CTX,
        n_threads=N_THREADS,
        # Set chat_format if your model supports it, e.g., 'llama-3'
        # chat_format="llama-3" 
    )

llm = load_model()

# === Data Processing Function (Cached) ===
@st.cache_data(show_spinner="Analyzing sentiment in uploaded file...")
def process_data(uploaded_file):
    """
    Reads an Excel file, analyzes sentiment for each review, and returns a DataFrame.
    This function is cached, so it only runs when the uploaded file changes.
    """
    df = pd.read_excel(uploaded_file)
    if "Review" not in df.columns:
        st.error("The uploaded Excel file must contain a column named 'Review'.")
        return None

    # --- Sentiment Analysis Step ---
    sentiments = []
    
    # Using st.status for a cleaner progress indicator
    with st.status("Analyzing sentiments...", expanded=True) as status:
        progress_bar = st.progress(0.0)
        total_reviews = len(df['Review'])

        for i, review in enumerate(df["Review"]):
            if pd.isna(review):
                sentiments.append("N/A")
                continue
            
            # This is a simple but effective prompt for classification
            prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a sentiment analysis expert. Classify the following review as 'Positive', 'Negative', or 'Neutral'. Respond with only one of those three words.<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Review: "{review}"
Sentiment:<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""
            
            output = llm(prompt, max_tokens=8, stop=["\n", "<|eot_id|>"])
            raw_sentiment = output["choices"][0]["text"].strip().capitalize()
            
            # Use regex for more robust matching
            if re.search(r'\bPositive\b', raw_sentiment, re.IGNORECASE):
                sentiments.append("Positive")
            elif re.search(r'\bNegative\b', raw_sentiment, re.IGNORECASE):
                sentiments.append("Negative")
            elif re.search(r'\bNeutral\b', raw_sentiment, re.IGNORECASE):
                sentiments.append("Neutral")
            else:
                sentiments.append("Unrecognized")
            
            # Update progress
            progress_bar.progress((i + 1) / total_reviews, text=f"Analyzing review {i+1}/{total_reviews}")
        
        status.update(label="Analysis complete!", state="complete")

    df["Sentiment"] = sentiments
    return df

# === Context Retrieval Function ===
def find_relevant_reviews(query: str, df: pd.DataFrame, max_samples=5) -> str:
    """
    Finds relevant review samples from the DataFrame based on the user's query.
    This is the "Retrieval" part of our RAG-lite system.
    """
    query = query.lower()
    relevant_df = pd.DataFrame()

    # Simple keyword-based retrieval
    if "negative" in query:
        relevant_df = df[df["Sentiment"] == "Negative"]
    elif "positive" in query:
        relevant_df = df[df["Sentiment"] == "Positive"]
    elif "neutral" in query:
        relevant_df = df[df["Sentiment"] == "Neutral"]

    # If specific sentiment is found, sample from it, otherwise sample from all data
    if not relevant_df.empty:
        # Take a sample, ensuring we don't exceed the number of available reviews
        num_samples = min(max_samples, len(relevant_df))
        sample_df = relevant_df.sample(n=num_samples, random_state=42)
    elif "review" in query or "customer" in query:
        # If no specific sentiment but the query seems data-related, provide a general sample
        num_samples = min(max_samples, len(df))
        sample_df = df.sample(n=num_samples, random_state=42)
    else:
        # If the query doesn't seem to be about the reviews, don't provide context
        return "No specific review data seems relevant to this query."

    # Format the samples into a string for the LLM prompt
    context_str = "Here are some relevant review samples:\n\n"
    for _, row in sample_df.iterrows():
        context_str += f"- Sentiment: {row['Sentiment']}\n  Review: \"{row['Review']}\"\n\n"
        
    return context_str.strip()

# === Streamlit App Layout ===
st.set_page_config(page_title="Data Chat Assistant", layout="wide")
st.title("📄💬 Chat with your Review Data (LLaMA 3.1)")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processed_df" not in st.session_state:
    st.session_state.processed_df = None

# === Sidebar for File Upload and Data Display ===
with st.sidebar:
    st.header("Upload & Analyze")
    uploaded_file = st.file_uploader(
        "Upload an Excel file with a 'Review' column",
        type=["xlsx"],
        key="file_uploader"
    )

    if uploaded_file:
        # The magic happens here: process_data is cached
        df = process_data(uploaded_file)
        if df is not None:
            st.session_state.processed_df = df
            st.success("File processed successfully!")

    if st.session_state.processed_df is not None:
        st.subheader("Sentiment Analysis Summary")
        summary_counts = st.session_state.processed_df["Sentiment"].value_counts()
        st.bar_chart(summary_counts)
        
        st.subheader("Analyzed Data")
        st.dataframe(st.session_state.processed_df)

# === Main Chat Interface ===
st.subheader("Ask Anything About the Reviews")

# Display prior chat messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if user_input := st.chat_input("Ask a question (e.g., 'Show me some negative reviews about the battery')"):
    # Add user message to history and display it
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Check if a file has been processed
    if st.session_state.processed_df is None:
        reply = "I'm ready to help, but you need to upload an Excel file with reviews first."
    else:
        # --- RAG in action! ---
        with st.spinner("Thinking..."):
            # 1. Retrieve relevant context
            df = st.session_state.processed_df
            relevant_context = find_relevant_reviews(user_input, df)
            
            # 2. Augment the prompt
            system_prompt = f"""You are a helpful data analyst assistant. Your task is to answer the user's questions based on the provided review data.
- First, use the 'Relevant Review Samples' to answer the question directly if possible.
- Second, use the 'Data Summary' for broader, quantitative questions.
- Be concise and base your answers on the data provided.
- If the data doesn't contain the answer, say so.
- Do not make up information.

---
DATA SUMMARY:
{df['Sentiment'].value_counts().to_string()}
---
RELEVANT REVIEW SAMPLES:
{relevant_context}
---
"""
            # Build conversation history for the model
            conversation = []
            for message in st.session_state.chat_history:
                conversation.append(message)
                
            # Use the Llama-3 chat template format for best results
            # Note: llama-cpp-python can do this automatically if you set `chat_format`
            # but doing it manually gives you more control.
            messages_for_llm = [
                {"role": "system", "content": system_prompt}
            ] + conversation

            # 3. Generate the response
            output = llm.create_chat_completion(
                messages=messages_for_llm,
                max_tokens=MAX_TOKENS_RESPONSE,
                stop=["<|eot_id|>"],
                temperature=0.7,
            )
            reply = output['choices'][0]['message']['content'].strip()

    # Add assistant reply to history and display it
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
