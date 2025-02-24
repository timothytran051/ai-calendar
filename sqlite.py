import sqlite3

conn = sqlite3.connect('calendar.db')

c = conn.cursor()

c.execute("""CREATE TABLE events (
    subject TEXT,
    date TEXT,
    category TEXT,
    reminder INTEGER,
    reccurence TEXT
    
)""")