from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import torch
from backend.config import HUGGINGFACE_TOKEN, CHAT_MODEL_NAME, CODE_MODEL_NAME  # ✅ Import model names from config

def load_model(model_name, purpose):
    """
    Loads an LLM with optimized memory usage.
    - `model_name`: Hugging Face model name.
    - `purpose`: "chat" for conversation, "code" for code generation.
    """
    try:
        print(f"🔄 Loading {model_name} ({purpose} model) with 4-bit quantization...")

        # **Enable 4-bit quantization to reduce memory usage**
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )

        # **Load tokenizer**
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            token=HUGGINGFACE_TOKEN
        )

        # **Load model with memory optimization**
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=quantization_config,
            device_map="auto",
            token=HUGGINGFACE_TOKEN
        )

        # **Create the pipeline**
        pipeline_type = "text-generation"
        model_pipeline = pipeline(pipeline_type, model=model, tokenizer=tokenizer)

        print(f"✅ {model_name} ({purpose} model) loaded successfully with 4-bit quantization!")
        return model_pipeline

    except Exception as e:
        print(f"❌ Error loading {model_name}: {e}")
        raise RuntimeError(f"Failed to load {model_name}. Check GPU memory availability.")

# **Load the chatbot model (For doubt resolution)**
chatbot = load_model(CHAT_MODEL_NAME, "chat")

# **Load the code generation model (For solutions)**
code_generator = load_model(CODE_MODEL_NAME, "code")
