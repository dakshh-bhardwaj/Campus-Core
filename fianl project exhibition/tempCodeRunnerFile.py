from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import csv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

DATABASE = 'students.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # Here you can handle user roles if needed
    return redirect(url_for('main'))

@app.route('/main')
def main():
    return render_template('main.html', students=get_students())

def get_students():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return students

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']
    student_class = request.form['class']
    contact = request.form['contact']
    hostel = request.form['hostel']
    mess = request.form['mess']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, class, contact, hostel, mess) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, age, student_class, contact, hostel, mess))
    conn.commit()
    conn.close()
    flash('Student added successfully!')
    return redirect(url_for('main'))

@app.route('/export_csv')
def export_csv():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    file_path = 'students.csv'
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Age", "Class", "Contact", "Hostel", "Mess"])
        writer.writerows(rows)

    return redirect(url_for('main'))

@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

@app.route('/remarks')
def remarks():
    return render_template('remarks.html')

if __name__ == '__main__':
    app.run(debug=True)