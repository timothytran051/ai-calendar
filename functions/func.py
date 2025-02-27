import fitz
import re
from sqlite import sql_class#, sql_date, sql_policy

date_pattern = r"""
            (?:\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*,\s)? # Matches optional weekday (e.g., "Tuesday, ")
            (?:\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{1,2}(?:,\s\d{4})?\b) | # Matches "May 13, 2025" or "May 13"
            (?:\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*,\s)? # Matches optional weekday again
            (?:\b\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}\b) | # Matches "2/25/25" or "02-25-2025"
            (?:\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*,\s)? # Matches optional weekday before this format
            (?:\b\d{1,2}(?:st|nd|rd|th)?(?:\sof)?\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s(?:\d{4})?\b) # Matches "13th of May" or "13th of May, 2025"
            """
event_pattern = r"\b(?:quiz|exam|midterm|final exam|test|assessment|homework|assignment|book report|paper|project|lab report|presentation)\b"
policy_pattern = r"(?:\b(?:drops?|removes?|excludes?)\s(?:one|two|three|\d+)?\s?(?:lowest|highest)?\s?(?:homework|assignment|quiz|exam|grade|score)s?\b)"



def extract_text(file_path):
    doc = fitz.open(file_path)
    full_text = " ".join([page.get_text("text") for page in doc])
    return full_text.replace("\n", " ").strip()


def extract_events(text):
    extracted_events = []
    if re.search(event_pattern, text, re.IGNORECASE):
        if re.search(date_pattern, text, re.IGNORECASE | re.VERBOSE):
                extracted_events.append(text)

    return extracted_events

def extract_policies(text):
    extracted_policies = []
    if re.search(policy_pattern, text, re.IGNORECASE | re.VERBOSE):
        extracted_policies.append(text)
        
    return extracted_policies

def convert(text):
    text_cleaned = text.strip()
    sections = text_cleaned.split("\n")
    class_name = sections[0].strip(' "“”')
    dates = [event.strip(' "“”') for event in sections[1:-1] if event.strip()]
    policy = sections[-1].strip(' "“”')
    # sql_class(class_name)
    
    print(dates)
    for date in dates:
         dates_new = date.split(":")

         print(dates_new[1].strip())
    # sql_date(dates)
    # sql_policy(policy)
    
