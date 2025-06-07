# Practice_KD
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chatbot Interface</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f4f4f4;
        }
        #chat-box {
            width: 100%;
            height: 400px;
            border: 1px solid #ccc;
            overflow-y: scroll;
            padding: 10px;
            background-color: #fff;
        }
        .message {
            margin: 5px 0;
        }
        .user {
            text-align: right;
            color: blue;
        }
        .bot {
            text-align: left;
            color: green;
        }
        #input-box {
            display: flex;
            margin-top: 10px;
        }
        #user-input {
            flex: 1;
            padding: 10px;
            font-size: 16px;
        }
        #send-button {
            padding: 10px;
            font-size: 16px;
            background-color: #007bff;
            color: white;
            border: none;
        }
    </style>
</head>
<body>

<h2>Chat with the MLOps Agent</h2>
<div id="chat-box"></div>

<div id="input-box">
    <input type="text" id="user-input" placeholder="Type your message here..." />
    <button id="send-button">Send</button>
</div>

<script>
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    function appendMessage(message, sender) {
        const div = document.createElement("div");
        div.classList.add("message", sender);
        div.innerText = message;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    sendButton.onclick = async () => {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage(message, "user");
        userInput.value = "";

        const response = await fetch("http://localhost:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `user_message=${encodeURIComponent(message)}`
        });

        const data = await response.json();
        appendMessage(data.response.content, "bot");
    };

    userInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendButton.click();
        }
    });
</script>

</body>
</html>


from fastapi import FastAPI, Form

@app.post("/chat")
async def chat_endpoint(user_message: str = Form(...)):
    global agent, messages
    messages.append({"role": "user", "content": user_message})
    response = run_full_turn(agent, messages)
    agent = response.agent
    messages.extend(response.messages)
    last_message = messages[-1]
    return {"response": last_message}


import streamlit as st
import requests

st.set_page_config(page_title="MLOps Chatbot", layout="centered")

st.title("🤖 MLOps Chatbot")

# Store chat history in session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.text_input("You:", key="user_input")

# When user hits enter or submits
if user_input:
    # Add user input to chat history
    st.session_state.chat_history.append(("user", user_input))

    # Send request to FastAPI backend
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            data={"user_message": user_input},
            timeout=5
        )
        data = response.json()
        bot_reply = data["response"]["content"]
    except Exception as e:
        bot_reply = f"[Error contacting backend: {e}]"

    # Add bot response to chat history
    st.session_state.chat_history.append(("bot", bot_reply))
    st.session_state.user_input = ""

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"<div style='text-align:right; color:blue;'>You: {message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align:left; color:green;'>Bot: {message}</div>", unsafe_allow_html=True)

