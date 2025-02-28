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
from functions.func import extract_text, extract_events, extract_policies, convert#, date_conversion

# _ = load_dotenv(find_dotenv())
# client = OpenAI(
#     api_key=os.environ.get('API_TOKEN')
# )

# model = "gpt-4o-mini"
# fileName = "pdfs/KINE 404 Syllabus SPR25 2025-01-21 - Tagged.pdf"
# fileName = "pdfs/CoursePolicies264.pdf"
# fileName = "pdfs/Spring 2025 CS 331 04 23988.pdf"
fileName = "pdfs/1 CHECKLIST_PHIL 348 (SP2025).pdf"

# print(pdf_text)
text = extract_text(fileName)
events_list = extract_events(text)
policies_list = extract_policies(text)

combined_output = events_list.copy()


if policies_list:
    combined_output.append("\n".join(policies_list))
else:
    combined_output.append("No drops found")

# print(combined_output)
response = ask_ai("\n".join(combined_output))
print(response)

# date_conversion(combined_output)
convert(response, combined_output)

# question = input("Calendar: ")
# response = ask_ai(question)
# print(response)