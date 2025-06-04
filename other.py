import os
import warnings

from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_core._api.deprecation import LangChainDeprecationWarning

warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

# API КЛЮЧ
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API")

# СТВОРЮЄМО ЛЛМ
llm = OpenAI(temperature=0)

# ПЕРЕВІРКА НА КИРИЛИЦЮ
def is_cyrillic(text: str) -> bool:
    return any('а' <= ch <= 'я' or 'А' <= ch <= 'Я' for ch in text)

def under(query: str) -> str:
    return "I'm sorry, I wasn't able to understand your request. I can only assist with topics related to cybersecurity, encryption methods, and encoding or decoding messages using one of the following five ciphers: Vigenère, Trithemius, Atbash, Caesar, or Daniel Defoe."








