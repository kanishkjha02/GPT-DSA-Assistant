from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.scraper import fetch_leetcode_problem # ✅ Import web scraper
from backend.model import chatbot  # ✅ Import chat model
import re  # ✅ Import regex for response validation

app = FastAPI()

# ✅ Request Model for Problem Analysis
class ProblemRequest(BaseModel):
    leetcode_slug: str  # Example: "two-sum"

# ✅ Request Model for Doubt Solving
class DoubtRequest(BaseModel):
    user_query: str
    problem_description: str

# ✅ Function to Clean and Validate Responses
def clean_and_validate_response(raw_response, prompt_text):
    """Cleans redundant text, ensures correct formatting, and validates completeness."""
    clean_text = raw_response.replace(prompt_text.strip(), "").strip()

    # **Check for common placeholders & reject if found**
    invalid_phrases = [
        "<Concise Explanation>", "<Step-by-step breakdown>", "Your turn!", 
        "Please provide your answer."
    ]
    if any(phrase in clean_text for phrase in invalid_phrases):
        return "Error: Response contained invalid placeholders. Regenerate."

    # **Ensure response contains time complexity information**
    if not re.search(r"O\(\s*[A-Za-z0-9^\(\)]+\s*\)", clean_text):
        return "Error: Time complexity missing. Regenerate."

    return clean_text if clean_text else "Error: Response was empty after cleaning."

# ✅ API to Fetch Problem Details & Generate Overview
@app.post("/analyze_problem/")
def analyze_problem(request: ProblemRequest):
    """
    Fetches problem details from LeetCode, extracts relevant data,
    and generates a beginner-friendly overview using Llama-2-7B-Chat.
    """
    # **Fetch problem details from LeetCode**
    problem_data = fetch_leetcode_problem(request.leetcode_slug)

    if "error" in problem_data:
        raise HTTPException(status_code=500, detail=problem_data["error"])

    # **Copy the DSA topics from scraped data**
    dsa_topics = problem_data["dsa_topics"]

    # **Generate Problem Overview using Llama-2-7B-Chat**
    try:
        prompt = f"""
        You are an AI assistant that explains coding problems.
        Given the following LeetCode problem, provide a structured and correct response.

        **Problem Title:** {problem_data['problem_title']}
        **Problem Statement:** {problem_data['problem_description']}

        ### **Instructions:**
        - Provide a **concise summary** of the problem.
        - Use the **correct algorithmic approach**.
        - Include **time complexity analysis**.
        - **Avoid placeholders** such as "<Concise Explanation>" or "<Step-by-step breakdown>".
        - Format the response properly for readability.

        **Your Response:**
        """

        response = chatbot(prompt, max_new_tokens=200, num_return_sequences=1)
        raw_response = response[0]["generated_text"].strip()

        # **Validate and Clean Response**
        clean_output = clean_and_validate_response(raw_response, prompt)
        if "Error" in clean_output:
            raise ValueError(clean_output)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate problem overview: {str(e)}")

    return {
        "problem_title": problem_data["problem_title"],
        "problem_overview": clean_output,  # ✅ Validated & Cleaned Response
        "dsa_topics": dsa_topics,  # ✅ Copied from web scraper
        "examples": problem_data["examples"]
    }

# ✅ API for Doubt Solving
@app.post("/solve_doubt/")
def solve_doubt(request: DoubtRequest):
    """Processes user doubts related to coding problems & generates accurate responses."""

    # **Reject Non-DSA Questions**
    forbidden_phrases = ["your name", "who are you", "what is your purpose"]
    if any(phrase in request.user_query.lower() for phrase in forbidden_phrases):
        return {"response": "I am an AI assistant specialized in coding. Please ask a DSA-related question."}

    # **Generate Contextual Query for LLM**
    prompt = f"""
    You are an AI assistant specializing in competitive programming and data structures & algorithms.

    **Problem:** {request.problem_description}
    **User's Question:** {request.user_query}

    ### **Instructions for Your Response:**
    - Use the **correct algorithmic approach**.
    - Include a **step-by-step breakdown** if needed.
    - Clearly state the **time complexity**.
    - Avoid introductions like "Sure, I'd be happy to help!"
    - Strictly **avoid incorrect algorithm choices**.
    - Format the response for **readability**.

    **Your Answer:**
    """

    try:
        # **Generate Response from LLM**
        response = chatbot(prompt, max_new_tokens=300, num_return_sequences=1)
        raw_response = response[0]["generated_text"].strip()

        # **Validate and Clean Response**
        clean_output = clean_and_validate_response(raw_response, prompt)
        if "Error" in clean_output:
            raise ValueError(clean_output)

        return {"response": clean_output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process doubt: {str(e)}")
