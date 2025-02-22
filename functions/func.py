import fitz
import re

def extract_text(file_path):
    doc = fitz.open(file_path)  # Open the PDF
    extracted_pages = []

    date_pattern = r"""
            (?:\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*,\s)? # Matches optional weekday (e.g., "Tuesday, ")
            (?:\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{1,2}(?:,\s\d{4})?\b) | # Matches "May 13, 2025" or "May 13"
            (?:\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*,\s)? # Matches optional weekday again
            (?:\b\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}\b) | # Matches "2/25/25" or "02-25-2025"
            (?:\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*,\s)? # Matches optional weekday before this format
            (?:\b\d{1,2}(?:st|nd|rd|th)?(?:\sof)?\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s(?:\d{4})?\b) # Matches "13th of May" or "13th of May, 2025"

            """
    event_pattern = r"\b(?:quiz|exam|midterm|final exam|test|assessment|homework|assignment|book report|paper|project|lab report|presentation)\b"

    for page in doc:
        text = page.get_text("text")
        text_cleaned = text.replace("\n", " ").strip()
        
        if re.search(event_pattern, text_cleaned, re.IGNORECASE):
            if re.search(date_pattern, text_cleaned, re.IGNORECASE | re.VERBOSE):
                extracted_pages.append(text_cleaned)
                
    return extracted_pages

