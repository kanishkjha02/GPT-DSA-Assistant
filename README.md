# 🧠 LeetCode GPT Teaching Assistant  

## 📌 Project Overview  
LeetCode GPT Teaching Assistant is an **AI-powered assistant** designed to help users **understand coding problems**, get **guided hints** instead of direct answers, and improve their **problem-solving skills**. This tool **analyzes LeetCode problems**, provides **insights into the problem**, and answers **user doubts** with structured explanations.

---

## 🏆 Author Details  
- **Name:** Kanishk Jha  
- **Email:** kanishkjha_co21a4_45@dtu.ac.in  
- **Roll No.:** 2K21/CO/219
- **LinkedIn:** [Kanishk Jha](https://www.linkedin.com/in/jha02--kanishk/)
- **Phone no.:** +91 7982571885

---

## 📝 Problem Statement  
LeetCode problems can sometimes be difficult to **understand and solve efficiently**. Beginners often need **guided hints** instead of direct solutions. Existing AI-based chatbots either:  
✅ **Give direct solutions (which kill learning)**  
✅ **Fail to provide meaningful guidance**  

Thus, we aim to create an **interactive teaching assistant** that:  
- **Analyzes** a LeetCode problem and explains the **underlying concept**.  
- **Generates useful hints** without giving away direct solutions.  
- **Provides structured insights**, including **time complexity analysis**.  
- **Fetches similar problems** from LeetCode for additional practice.  

---

## 🎯 Our Solution Approach  
### **1️⃣ Problem Analysis (Backend)**  
- We **fetch problem details** from LeetCode using **GraphQL API**.  
- The extracted data includes:  
  - **Problem title, description, and examples**  
  - **DSA topics covered**  
  - **List of similar problems**  

### **2️⃣ Doubt Solving (AI Model)**  
- Uses a **fine-tuned GPT model** to provide **guided hints** rather than direct solutions.  
- **Ensures correct algorithm selection** (e.g., HashMap for Two Sum, DP for Knapsack).  
- **Formats responses properly**, including **step-by-step breakdowns** and **time complexity analysis**.  

### **3️⃣ User Interface (Frontend - Streamlit)**  
- Users **enter a LeetCode problem link** → GPT fetches problem details & provides hints.  
- Users **ask doubts** → The AI **answers with explanations, not just solutions**.  
- Users **explore similar problems** → Helps them **practice related concepts**.  

---

## 📜 Project Requirements  
To run this project, make sure you have the following dependencies installed:  

### **Frontend (Streamlit) Requirements**  
```bash
pip install -r frontend/requirements.txt
```

### **Backend (FastAPI) Requirements**  
```bash
pip install -r backend/requirements.txt
```

---

## 🚀 How to Run the Application  
### **Step 1: Clone the Repository**  
```bash
git clone https://github.com/your-repo/LeetCode-GPT-Assistant.git
cd LeetCode-GPT-Assistant
```

### **Step 2: Set Up the Backend**  
1️⃣ **Navigate to the backend directory:**  
```bash
cd backend
```
2️⃣ **Set Up Your Hugging Face API Token**  
- Open the **`.env` file** in the `backend` directory.
- Add your **Hugging Face API token**:
  ```bash
  HUGGINGFACE_ACCESS_TOKEN="your-huggingface-token-here"
  ```
- This token is required to interact with the GPT model.

3️⃣ **Run the FastAPI server:**  
```bash
uvicorn main:app --reload
```
- This will start the API on `http://127.0.0.1:8000`.

### **Step 3: Set Up the Frontend**  
1️⃣ **Navigate to the frontend directory:**  
```bash
cd frontend
```
2️⃣ **Run the Streamlit app:**  
```bash
streamlit run app.py
```
- The assistant will be accessible on `http://localhost:8501`.

---

## 🔑 Authentication with Hugging Face API  
Since this project **uses a Hugging Face model for text generation**, you **must provide your Hugging Face API token** to fetch AI-generated responses.

To do this:  
1. Go to **[Hugging Face](https://huggingface.co/settings/tokens)** and create a **new access token**.
2. Copy the token and **paste it into `backend/.env` file** as follows:
   ```bash
   HUGGINGFACE_ACCESS_TOKEN="your-huggingface-token-here"
   ```
3. Restart the backend server.

⚠️ **Without this token, AI-generated responses will not work!**  

---

## 🎥 Demo Video  
For a **detailed demo of how the assistant works**, watch the video here:  
📌 **[Demo Video](https://drive.google.com/file/d/17WAd6_ooS6jRNvE4-Vs0op0yfoCgBNdi/view?usp=sharing)**  

---

## 💡 Future Improvements  
- Implement Similar Problems feature.
- Add **voice-based interaction** using Speech-to-Text.  
- Implement **a leaderboard** to track problem-solving progress.  
- Support **multiple programming languages** for custom solutions.  

---

## 🛠️ Tech Stack Used  
- **Frontend:** Streamlit  
- **Backend:** FastAPI  
- **AI Model:** Hugging Face GPT-based Model  
- **Web Scraping:** BeautifulSoup & Selenium  
- **Database:** SQLite (Future Expansion)  

---

## 🤝 Contributing  
Want to improve this project? Follow these steps:  
1. **Fork the repository**  
2. **Create a feature branch:**  
   ```bash
   git checkout -b feature-new
   ```
3. **Make your changes & commit:**  
   ```bash
   git commit -m "Added new feature"
   ```
4. **Push to GitHub & submit a PR:**  
   ```bash
   git push origin feature-new
   ```

---

## 📜 License  
This project is open-source under the **MIT License**.

---

### ✅ **Star ⭐ this repository if you found it helpful!** 🚀  
