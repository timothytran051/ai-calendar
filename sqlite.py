import sqlite3
# from functions.func import extract_events, extract_policies

conn = sqlite3.connect('calendar.db')

c = conn.cursor()

def get_class_id(class_name):
    c.execute("SELECT id FROM classes WHERE class_name = ?", (class_name.strip(),))
    result = c.fetchone()
    return result[0] if result else None

def sql_class(text):
    try:
        c.execute("INSERT OR IGNORE INTO classes (class_name) VALUES (?)", (text,))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Class '{text}' already exists. Skipping insert.")

def sql_date(class_id, event, start, end):
    c.execute("""
        SELECT start_date, end_date FROM events 
        WHERE class_id = ? AND event_name = ? 
    """, (class_id, event))
    
    existing_event = c.fetchone()

    if existing_event:
        existing_start, existing_end = existing_event


        existing_start = existing_start if existing_start else start
        existing_end = existing_end if existing_end else end


        new_start = min(existing_start, start) if existing_start and start else existing_start or start

        new_end = max(existing_end, end) if existing_end and end else existing_end or end

        if (new_start, new_end) != (existing_start, existing_end):
            c.execute("""
                UPDATE events 
                SET start_date = ?, end_date = ?
                WHERE class_id = ? AND event_name = ?
            """, (new_start, new_end, class_id, event))
            
            print(f"Updated event: {event} to {new_start} - {new_end}")
        else:
            print(f"No change needed for {event}")

    else:
        c.execute("""
            INSERT INTO events (class_id, event_name, start_date, end_date) 
            VALUES (?, ?, ?, ?)
        """, (class_id, event, start, end))
        print(f"Inserted new event: {event} on {start} - {end}")

    conn.commit()

def sql_policy(text):
    c.execute("""INSERT INTO policies (drop_type) VALUES (?)""", (text))
    conn.commit()

def sql_syllabus(class_id, syllabus_text):
    c.execute("""INSERT INTO syllabi (class_id, syllabus_text) VALUES (?, ?)""", (class_id, syllabus_text))
    conn.commit()

def sql_ai(class_id, processed_text):
    c.execute("""INSERT INTO ai (class_id, extracted_text) VALUES (?, ?)""", (class_id, processed_text))
    conn.commit()

# c.execute("""CREATE TABLE classes(
#           id INTEGER PRIMARY KEY,
#           class_name TEXT UNIQUE
#           )""")

# c.execute("""CREATE TABLE events (
#     id INTEGER PRIMARY KEY,
#     class_id INTEGER,
#     event_name TEXT,
#     start_date TEXT,
#     end_date TEXT,
#     reminder INTEGER,
#     outlook_id TEXT,
#     FOREIGN KEY (class_id) REFERENCES classes (id)
    
# )""")

# c.execute("""CREATE TABLE reccuring_tasks (
#           id INTEGER PRIMARY KEY,
#           class_id INTEGER,
#           task_name TEXT,
#           due_time TEXT,
#           reccurence TEXT,
#           reminder INTEGER,
#           FOREIGN KEY (class_id) REFERENCES classes (id)
# )""")

# c.execute("""CREATE TABLE policies (
#           id INTEGER PRIMARY KEY,
#           class_id INTEGER,
#           drop_type TEXT,
#           drop_count INTEGER,
#           FOREIGN KEY (class_id) REFERENCES classes (id)
# )""")

# # c.execute("""CREATE TABLE syllabi(
#     id INTEGER PRIMARY KEY,
#     class_id INTEGER,
#     syllabus_text TEXT,
#     FOREIGN KEY (class_id) REFERENCES classes (id)
#           )""")

# c.execute("""CREATE TABLE ai(
#             id INTEGER PRIMARY KEY,
#             class_id INTEGER,
#             extracted_text TEXT,
#             processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (class_id) REFERENCES classes (id)
# )""")

tables = ["classes", "events", "syllabi", "ai"]
for table in tables:
    print(f"\n--- {table.upper()} TABLE ---")
    c.execute(f"SELECT * FROM {table}")
    rows = c.fetchall()
    for row in rows:
        print(row)

c.execute("DELETE FROM events")
conn.commit()
c.execute("DELETE FROM ai")
conn.commit()