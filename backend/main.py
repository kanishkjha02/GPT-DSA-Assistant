from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

# Initialize FastAPI app
app = FastAPI()

# Load Mistral-7B Model
MODEL_NAME = "mistralai/Mistral-7B"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, device_map="auto")
chatbot = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Define request format
class ChatRequest(BaseModel):
    user_query: str
    problem_description: str

# Chat endpoint
@app.post("/chat/")
def chat_with_gpt(request: ChatRequest):
    try:
        prompt = f"Given the following DSA problem: {request.problem_description}, \
        the user has asked: {request.user_query}. \
        Provide step-by-step hints and questions to guide them without giving a direct answer."
        
        response = chatbot(prompt, max_length=256, num_return_sequences=1)
        return {"response": response[0]["generated_text"]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
