import os
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from ai.ai_processor import ask_ai

_ = load_dotenv(find_dotenv())
# client = OpenAI(
#     api_key=os.environ.get('API_TOKEN')
# )

# model = "gpt-4o-mini"

question = input("Calendar: ")
response = ask_ai(question)
print(response)