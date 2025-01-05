import sqlite3, os

churchDB = r"C:\Users\mmcel\Downloads\Bladensburg\ChildrenChurch.db"

# Check if file exists and delete it 
if os.path.exists(churchDB): 
    os.remove(churchDB) 
    print(f"{churchDB} has been deleted.")
else: 
    print(f"{churchDB} does not exist.")

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(churchDB)
cursor = conn.cursor()

# Create the Registered table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Registered (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    ParentName TEXT NOT NULL,
    ParentEmail TEXT NOT NULL,
    Birthdate DATE NOT NULL,
    CurriculumConsent BOOLEAN NOT NULL CHECK (CurriculumConsent IN (0, 1)),
    SafetyConsent BOOLEAN NOT NULL CHECK (SafetyConsent IN (0, 1)),
    Allergies TEXT
)
''')

# Create the Allergy table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Allergy (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Allergy TEXT NOT NULL
)
''')

# Insert rows into the Allergy table
allergies = ['Peanuts', 'Milk', 'Fish', 'Chocolate', 'Pork', 'Sugar']
for allergy in allergies:
    cursor.execute('''
    INSERT INTO Allergy (Allergy) VALUES (?)
    ''', (allergy,))

# Create the Roll_Sheet table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Roll_Sheet (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    StudentName TEXT NOT NULL,
    Date TEXT NOT NULL,
    TimeIn TEXT NOT NULL,
    DroppedBy TEXT NOT NULL,
    TimeOut TEXT,
    PickUpBy TEXT
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
