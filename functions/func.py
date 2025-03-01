import fitz
import re
from datetime import datetime, timedelta
from sqlite import sql_class, sql_date, get_class_id, sql_syllabus, sql_ai#, sql_policy
from ai.ai_processor import ask_ai

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

def convert(text, syllabus_text):
    text_cleaned = text.strip()
    sections = text_cleaned.split("\n")
    class_name = sections[0].strip(' "“”')
    dates = [event.strip(' "“”') for event in sections[1:-1] if event.strip()]
    policy = sections[-1].strip(' "“”')
    sql_class(class_name)

    # class_id = get_class_id(class_name)
    # if class_id:
    #     sql_syllabus(class_id, syllabus_text)
    #     sql_ai(class_id, text)
    # else:
    #     print(f"Class '{class_name}' not found in database.")

    for date in dates:
        date_sections = date.split(":")
        event_name = date_sections[0].strip()
        event_date = date_sections[1].strip()
        temp = event_name.lower().strip()
        if "midterm" in temp:
            event_name = "Exam 1"
        if "final" in temp:
            event_name = "Exam X"


        if "_" in event_date:
            start_date, end_date = event_date.split("_", maxsplit = 1)
            start_date, end_date = start_date.strip(), end_date.strip()
        else:
            start_date, end_date = event_date.strip(), None
        

        if "Week" in start_date:
            start_date = convert_week_to_date(start_date)
        if end_date and "Week" in end_date:
            end_date = convert_week_to_date(end_date)

        class_id = get_class_id(class_name)
        if class_id:
            sql_date(class_id, event_name, start_date, end_date)
        else:
            print(f"Class '{class_name}' not found in database.")
    

def convert_week_to_date(text):
    semester_start = datetime(2025, 1, 21)
    try:
        week_num = int(text.replace("Week", "").strip())
    except ValueError:
        return None

    calculated_date = semester_start + timedelta(weeks=(week_num - 1))
    return calculated_date.strftime("%Y-%m-%d")



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
convert(response, "\n".join(combined_output))

# question = input("Calendar: ")
# response = ask_ai(question)
# print(response)