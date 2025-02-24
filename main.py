import os
import pymupdf
import re
import fitz
import pdfplumber
import pandas as pd
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from ai.ai_processor import ask_ai
from functions.func import extract_text, extract_events, extract_policies

_ = load_dotenv(find_dotenv())
# client = OpenAI(
#     api_key=os.environ.get('API_TOKEN')
# )

# model = "gpt-4o-mini"
# fileName = "pdfs/KINE 404 Syllabus SPR25 2025-01-21 - Tagged.pdf"
# fileName = "pdfs/CoursePolicies264.pdf"
# fileName = "pdfs/Spring 2025 CS 331 04 23988.pdf"
fileName = "pdfs/1 CHECKLIST_PHIL 348 (SP2025).pdf"


# with pdfplumber.open(fileName) as pdf:
#     for page in pdf.pages:
#         text = page.extract_text()
#         match = re.search(r"exam", text, re.IGNORECASE)
#         if match:
#             pattern = r"""
#             (?:\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{1,2},\s\d{4}\b) | # March 15, 2025
#             (?:\b\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}\b) | # 03/15/25 or 15-03-2025
#             (?:\b\d{1,2}(?:st|nd|rd|th)?\s(?:of\s)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b) # 15th of March
#             """
#             match1 = re.findall(pattern, text, re.IGNORECASE | re.VERBOSE)
#             if match1:
#                 text.replace("\n", " ")
#                 # response = ask_ai(text)
#                 # print(response)
#                 print(text)
#             # print(text)
#             # print("Exam found")

# print(pdf_text)
text = extract_text(fileName)
events = extract_events(text)
policies = extract_policies(text)

print(policies)
# response = ask_ai(policies)
# print(response)




# question = input("Calendar: ")
# response = ask_ai(question)
# print(response)