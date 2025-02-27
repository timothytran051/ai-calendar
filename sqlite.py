import sqlite3
# from functions.func import extract_events, extract_policies

conn = sqlite3.connect('calendar.db')

c = conn.cursor()

def sql_class(text):
    try:
        c.execute("INSERT INTO classes (class_name) VALUES (?)", (text,))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Class '{text}' already exists. Skipping insert.")

# def sql_date(text):
    



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
#           class_id TEXT,
#           drop_type TEXT,
#           drop_count INTEGER,
#           FOREIGN KEY (class_id) REFERENCES classes (id)
# )""")

