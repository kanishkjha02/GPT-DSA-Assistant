import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Secure Hugging Face Token
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "your-default-token")

# Define Chat Model Name
CHAT_MODEL_NAME = "meta-llama/Llama-2-7B-chat-hf"

# Define Code Model Name
CODE_MODEL_NAME = "codellama/CodeLlama-7B-Python-hf"
