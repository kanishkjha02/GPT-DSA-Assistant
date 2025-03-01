import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/chat/"

st.title("📚 GPT-Powered DSA Teaching Assistant")
st.write("Ask questions about a LeetCode problem, and get hints!")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input for problem URL & question
leetcode_link = st.text_input("🔗 LeetCode Problem URL")
user_query = st.text_area("💬 Your Question")

if st.button("Get Hints"):
    if leetcode_link and user_query:
        # Mock problem description (API integration for scraping can be added)
        problem_description = "This is a sample DSA problem extracted from the link."
        
        # API request to FastAPI backend
        response = requests.post(API_URL, json={"user_query": user_query, "problem_description": problem_description})
        
        if response.status_code == 200:
            bot_reply = response.json().get("response", "Error generating response")
            st.session_state.messages.append({"role": "user", "content": user_query})
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        else:
            st.error("Error fetching response from the API")

# Display chat history
for msg in st.session_state.messages:
    st.write(f"**{msg['role'].capitalize()}:** {msg['content']}")
