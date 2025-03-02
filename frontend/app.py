import streamlit as st
import requests

# FastAPI Backend URL
API_URL = "http://127.0.0.1:8000"

# Set Page Configuration
st.set_page_config(page_title="📚 DSA GPT Assistant", layout="wide")

# Title
st.title("📚 GPT-Powered DSA Teaching Assistant")
st.write("Analyze a LeetCode problem and get structured guidance!")

# **Step 1: Enter LeetCode Problem URL**
st.subheader("🔍 Analyze a LeetCode Problem")
leetcode_link = st.text_input("🔗 Enter LeetCode Problem URL (e.g., https://leetcode.com/problems/two-sum/)")

if st.button("Analyze Problem"):
    if leetcode_link:
        leetcode_slug = leetcode_link.rstrip("/").split("/")[-1]  # Extract problem slug from URL

        with st.spinner("🔍 Analyzing problem... Please wait"):
            response = requests.post(f"{API_URL}/analyze_problem/", json={"leetcode_slug": leetcode_slug})
        
        if response.status_code == 200:
            problem_data = response.json()

            # Store in session state
            st.session_state["problem_title"] = problem_data["problem_title"]
            st.session_state["problem_overview"] = problem_data["problem_overview"]
            st.session_state["problem_topics"] = problem_data["dsa_topics"]
            st.session_state["examples"] = problem_data["examples"]
            st.session_state["problem_analyzed"] = True

        else:
            st.error("❌ Error analyzing problem. Please try again.")

# **Step 2: Display Problem Details**
if st.session_state.get("problem_analyzed"):
    st.subheader(f"📌 {st.session_state['problem_title']}")
    st.markdown(f"**Overview:**\n\n{st.session_state['problem_overview']}")

    st.subheader("📂 Topics Covered")
    st.write(", ".join(st.session_state["problem_topics"]))

    st.subheader("📌 Examples")
    for example in st.session_state["examples"]:
        for key, value in example.items():
            st.markdown(f"**{key}**")
            st.markdown(f"📝 **Input:** `{value['input']}`")
            st.markdown(f"✅ **Expected Output:** `{value['expected_output']}`\n")

    # **Step 3: Ask Doubts**
    st.subheader("❓ Ask Your Doubt About This Problem")
    user_query = st.text_area("💬 Enter Your Doubt")

    if st.button("Ask Doubt"):
        if user_query:
            with st.spinner("⏳ Processing your question..."):
                response = requests.post(f"{API_URL}/solve_doubt/", json={
                    "user_query": user_query,
                    "problem_description": st.session_state["problem_overview"]
                })

            if response.status_code == 200:
                bot_reply = response.json().get("response", "❌ Error generating response")
                st.session_state["chat_history"] = st.session_state.get("chat_history", []) + [
                    {"role": "assistant", "content": bot_reply}
                ]
            else:
                st.error("❌ Error fetching response.")

    # Display Chat History
    for msg in st.session_state.get("chat_history", []):
        with st.chat_message("assistant"):
            st.write(msg["content"])

    # **Step 4: Similar Problems Button**
    if st.button("🔗 Get Similar Problems"):
        st.warning("⚠️ This feature will be added soon!")
