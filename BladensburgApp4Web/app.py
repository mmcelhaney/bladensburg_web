from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import subprocess
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

current_directory = os.getcwd()
print(f"Current Directory: {current_directory}")
# Create a new sqlite file path
new_db_path = os.path.join(current_directory, 'ChildrenChurch.db')
print(f"New File Path: {new_db_path}")

def create_database():
    try:
        if not os.path.exists(new_db_path):
            subprocess.run(["python", "Create_Children_Church_Database.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Database creation failed: {e}")

def check_and_create_database():
    try:
        create_database()
    except Exception as e:
        print(f"Database creation failed: {e}")

@app.route('/')
def splash():
    return render_template('KingdomKidsMinistry_splash.htm')

@app.route('/KingdomKidsMinistry_RollsheetForm.htm', methods=['GET', 'POST'])
def rollsheet():
    conn = sqlite3.connect(new_db_path)
    c = conn.cursor()
    c.execute('SELECT StudentName FROM Roll_Sheet')
    students = c.fetchall()
    conn.close()
    
    if request.method == 'POST':
        if 'sign_in' in request.form:
            student_name = request.form['comboBoxStudentName']
            date = request.form['dateEdit']
            time_in = datetime.now().strftime('%H:%M:%S')
            parent_in = request.form['textParentInEdit']
            
            conn = sqlite3.connect(new_db_path)
            c = conn.cursor()
            c.execute('INSERT INTO Roll_Sheet (StudentName, Date, TimeIn, DroppedBy) VALUES (?, ?, ?, ?)', (student_name, date, time_in, parent_in))
            conn.commit()
            conn.close()
        elif 'sign_out' in request.form:
            student_name = request.form['comboBoxStudentName']
            time_out = datetime.now().strftime('%H:%M:%S')
            parent_out = request.form['textParentOutEdit']
            
            conn = sqlite3.connect(new_db_path)
            c = conn.cursor()
            c.execute('UPDATE Roll_Sheet SET TimeOut = ?, PickedUpBy = ? WHERE StudentName = ? AND Date = ?', (time_out, parent_out, student_name, datetime.now().strftime('%Y-%m-%d')))
            conn.commit()
            conn.close()
        elif 'add_student' in request.form:
            return redirect(url_for('pswd_form'))
        elif 'quit' in request.form:
            return redirect(url_for('goodbye'))
    
    return render_template('KingdomKidsMinistry_RollsheetForm.htm', students=[student[0] for student in students], date=datetime.now().strftime('%Y-%m-%d'))

@app.route('/KingdomKidsMinistry_PswdForm.htm', methods=['GET', 'POST'])
def pswd_form():
    if request.method == 'POST':
        password = request.form['txtPassword']
        if password == '1234':
            return redirect(url_for('register_student'))
        else:
            flash('Wrong Password')
            return redirect(url_for('pswd_form'))
    return render_template('KingdomKidsMinistry_PswdForm.htm')

@app.route('/KingdomKidsMinistry_Register.htm', methods=['GET', 'POST'])
def register_student():
    conn = sqlite3.connect(new_db_path)
    c = conn.cursor()
    c.execute('SELECT Allergy FROM Allergy')
    allergies = c.fetchall()
    conn.close()

    if request.method == 'POST':
        if 'save' in request.form:
            last_name = request.form['txtLastName']
            first_name = request.form['txtFirstName']
            parent_name = request.form['txtParentName']
            parent_email = request.form['textParentEmail']
            birthdate = request.form['dateEdit']
            curriculum_consent = 'True' if 'chkBoxParentalConsent_1' in request.form else 'False'
            safety_consent = 'True' if 'chkBoxParentalConsent_2' in request.form else 'False'
            allergies = request.form.getlist('listAllergies')

            conn = sqlite3.connect(new_db_path)
            c = conn.cursor()
            c.execute('INSERT INTO Registered (LastName, FirstName, ParentName, ParentEmail, Birthdate, CurriculumConsent, SafetyConsent, Allergies) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                      (last_name, first_name, parent_name, parent_email, birthdate, curriculum_consent, safety_consent, ','.join(allergies)))
            conn.commit()
            conn.close()
        elif 'clear' in request.form:
            # Just re-render the template to clear the form
            return redirect(url_for('register_student'))
        elif 'rolls_form' in request.form:
            return redirect(url_for('rollsheet'))
        elif 'send_email' in request.form:
            return redirect(url_for('email_window'))

    return render_template('KingdomKidsMinistry_Register.htm', allergies=[allergy[0] for allergy in allergies])

@app.route('/KingdomKidsMinistry_EmailWindow.htm', methods=['GET', 'POST'])
def email_window():
    if request.method == 'POST':
        if 'send_email' in request.form:
            from_email = request.form['txtfromEmail']
            email_text = request.form['txtEmailText']

            # Fetch all parent emails from Registered table
            conn = sqlite3.connect(new_db_path)
            c = conn.cursor()
            c.execute('SELECT ParentEmail FROM Registered')
            emails = [email[0] for email in c.fetchall()]
            conn.close()

            # Send email to all parents
            msg = MIMEText(email_text)
            msg['Subject'] = 'Important Update from Kingdom Kids Ministry'
            msg['From'] = from_email
            msg['To'] = ', '.join(emails)

            # Replace 'your_smtp_server' with your actual SMTP server and 'your_email' with your email address
            with smtplib.SMTP('your_smtp_server') as server:
                server.login('your_email', 'your_password')
                server.sendmail(from_email, emails, msg.as_string())

            flash('Email sent successfully!')
            return redirect(url_for('email_window'))
        elif 'return_to_registry' in request.form:
            return redirect(url_for('register_student'))
    
    return render_template('KingdomKidsMinistry_EmailWindow.htm')

@app.route('/goodbye')
def goodbye():
    return render_template('goodbye.html')

if __name__ == '__main__':
    check_and_create_database()
    app.run(debug=True)
