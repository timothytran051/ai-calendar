import sqlite3

conn = sqlite3.connect('calendar.db')

c = conn.cursor()

c.execute("""CREATE TABLE calendar (
    class_name TEXT,
    exam_date TEXT,
    
)""")