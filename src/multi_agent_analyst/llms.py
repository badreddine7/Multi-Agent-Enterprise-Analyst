from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def get_gemini_llm(max_output_tokens: int = 1200):
    return ChatGroq(
        model="llama-3.1-8b-instant", 
        api_key=""
    )
