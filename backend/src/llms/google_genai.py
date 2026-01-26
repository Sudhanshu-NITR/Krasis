import os
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from config.settings import (
    GOOGLE_API_KEY, 
    CHAT_MODEL_NAME
)

def get_google_genai_llm(model: str = CHAT_MODEL_NAME, temperature: float = 0.2):
    """
    Initializes a Google Gemini LLM with safety settings suitable for 
    technical documentation and code generation.
    """

    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    
    model = ChatGoogleGenerativeAI(
        model = model,
        temperature=temperature,
        api_key=GOOGLE_API_KEY,
        streaming=True,
        # Safety settings are crucial for code-related tasks to prevent 
        # false positives in blocking technical snippets.
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        },
    )

    return model