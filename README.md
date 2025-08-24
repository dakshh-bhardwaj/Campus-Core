# Student Management System (CustomTkinter, SQLite)

A desktop Student Management System built with Python and CustomTkinter that supports role selection (Admin/Hostel/Mess), student records management (add/view/export), attendance tracking, and remarks management, backed by a local SQLite database.

## Features

- Role selection at login: Admin, Hostel, Mess (demo role picker)
- Student records management:
  - Add students with fields: Name, Age, Class, Contact, Hostel, Mess
  - View students in a styled table (ttk Treeview)
  - Export students to CSV
- Attendance management:
  - Mark attendance by date for each student
  - Save attendance to SQLite
  - Download attendance CSV for a selected date
- Remarks management:
  - Add remarks per student
  - View all remarks for a selected student
- Analytics:
  - Bar chart: Students per Hostel (Matplotlib)
- UI/UX:
  - CustomTkinter modern UI (light/dark/system modes)
  - Indeterminate loading screen on startup
  - Themed headers and styled tables
- Reliable local persistence with SQLite and safe table creation

## Tech Stack

- Python 3.x
- CustomTkinter, Tkinter/ttk
- SQLite3
- Matplotlib
- CSV utilities

## Project Structure

- Loading window (splash): starts the app with a progress bar
- DatabaseManager: initializes SQLite tables (students, attendance, remarks)
- LoginWindow: role selector (Admin/Hostel/Mess) and bootstrap to main app
- MainWindow: core CRUD UI, export, graphs, navigation to submodules
- AttendanceWindow: mark/download attendance by date
- RemarksWindow: add/list remarks per student

## Database Schema

Tables created automatically on first run:

- students
  - id INTEGER PRIMARY KEY AUTOINCREMENT
  - name TEXT
  - age INTEGER
  - class TEXT
  - contact TEXT
  - hostel TEXT
  - mess TEXT
- attendance
  - id INTEGER PRIMARY KEY AUTOINCREMENT
  - student_id INTEGER REFERENCES students(id)
  - date TEXT (YYYY-MM-DD)
  - status TEXT (“Present”/“Absent”)
- remarks
  - id INTEGER PRIMARY KEY AUTOINCREMENT
  - student_id INTEGER REFERENCES students(id)
  - remark TEXT

## Getting Started

### Prerequisites

- Python 3.8+ recommended

### Installation

1. Clone the repository:
   - git clone <your-repo-url>
   - cd <repo-folder>

2. Create and activate a virtual environment (optional but recommended):
   - python -m venv .venv
   - Windows: .venv\Scripts\activate
   - macOS/Linux: source .venv/bin/activate

3. Install dependencies:
   - pip install customtkinter matplotlib

   Note: tkinter ships with most Python distributions. If missing, install via system package manager (e.g., sudo apt-get install python3-tk on Debian/Ubuntu).

### Run

- python app.py
  - The app opens with a splash/loading screen, then the Role selection window.
  - Choose a role to open the main window.
  - Add students, manage attendance/remarks, export CSV, and view graphs.

If your main file has a different name, run:
- python <filename>.py

## Usage Guide

- Add Student: Fill all fields and click “Add Student”.
- Clear Fields: Resets input entries.
- Export to CSV: Save all student records to a CSV file.
- Show Graph: Displays bar chart of student count per hostel.
- Manage Attendance:
  - Enter date (YYYY-MM-DD), click “Mark Attendance”.
  - Check students as present (unchecked = absent).
  - Click “Update Attendance” to save.
  - To download, enter the same date and click “Download Attendance”.
- Manage Remarks:
  - Select a student from the dropdown.
  - Enter a remark, click “Add Remark”.
  - Click “Show Remarks” to list all remarks for that student.

## Screens and Components

- Loading: small window with indeterminate progress bar
- LoginWindow: simple role selection (Admin/Hostel/Mess)
- MainWindow:
  - Header with app title
  - Input form (Name, Age, Class, Contact, Hostel, Mess)
  - Actions: Add, Clear, Export, Show Graph, Manage Attendance, Manage Remarks
  - Table view for students (Treeview)
- AttendanceWindow:
  - Date entry
  - Dynamic list of students with checkboxes
  - Update Attendance, Download Attendance (CSV)
- RemarksWindow:
  - Student selector (ComboBox)
  - Add and display remarks
  - Scrollable table for remarks

## Notes and Best Practices

- Input validation:
  - Name is required
  - Age and Contact must be numeric
- Date format:
  - Use YYYY-MM-DD for attendance
- CSV export:
  - Prompts a save dialog; ensure write permissions to chosen path
- UI behavior:
  - Attendance/Remarks windows stay on top for better task focus

## Troubleshooting

- Missing tkinter:
  - Install via system package manager or use a Python distribution that includes it.
- Database errors:
  - Ensure the app has write permissions in the working directory (creates students.db).
- Matplotlib backend issues:
  - If running in a headless environment, run locally with a desktop session.

## Roadmap (Optional Enhancements)

- Role-based permissions (actual RBAC for Admin/Hostel/Mess)
- Edit/Delete student records
- Attendance summaries and monthly reports
- Import students from CSV
- Search/filter in the students table
- Packaging as an executable (PyInstaller)

## License

Specify your license here (e.g., MIT). Include a LICENSE file in the repo.

## Acknowledgments

- CustomTkinter for a modern Tkinter UI experience
- Python’s standard library (sqlite3, csv) and Matplotlib for visualization

## How to Contribute

- Open issues for bugs/feature requests
- Submit PRs with clear descriptions and tested changes

***

Made with Python and CustomTkinter.
