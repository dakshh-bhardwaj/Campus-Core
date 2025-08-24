import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import matplotlib.pyplot as plt
import csv
# import loading2

import sys
import customtkinter as ctk


class Loading(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Set window properties
        self.geometry("460x100+500+300")
        self.title("Student Management System")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: sys.exit())
        ctk.set_appearance_mode("system")  # "light" or "dark"
        ctk.set_default_color_theme("blue")  # Use blue theme
        
        self.screen()
        self.mainloop()

    def screen(self):
        # Add components
        self.label = ctk.CTkLabel(self, text="Loading...", font=("Cambria", 17))
        self.label.place(x=20, y=10)

        self.progressbar = ctk.CTkProgressBar(self, width=400, mode="indeterminate")
        self.progressbar.place(x=20, y=50)
        self.progressbar.start()

        self.after(3110, self.get)  # Trigger get() after 3110 ms

    def get(self):
        self.progressbar.stop()
        self.destroy()


if __name__ == "__main__":
    Loading()


# l = loading2.Loading()


class DatabaseManager:
    """Class to handle database initialization and operations."""

    @staticmethod
    def init_db():
        try:
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    class TEXT,
                    contact TEXT,
                    hostel TEXT,
                    mess TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    date TEXT,
                    status TEXT,
                    FOREIGN KEY (student_id) REFERENCES students(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS remarks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    remark TEXT,
                    FOREIGN KEY (student_id) REFERENCES students(id)
                )
            """)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error initializing database: {e}")


class LoginWindow:
    """Login Window for selecting user role."""
    def __init__(self):
        self.login_window = ctk.CTk()
        self.login_window.title("Login")
        self.login_window.geometry("400x300")

        label = ctk.CTkLabel(self.login_window, text="Select Role", font=("Helvetica", 20))
        label.pack(pady=20)

        ctk.CTkButton(self.login_window, text="Admin", command=self.open_main_window).pack(pady=10)
        ctk.CTkButton(self.login_window, text="Hostel", command=self.open_main_window).pack(pady=10)
        ctk.CTkButton(self.login_window, text="Mess", command=self.open_main_window).pack(pady=10)

        self.login_window.mainloop()

    def open_main_window(self):
        self.login_window.destroy()
        MainWindow()


class MainWindow:
    """Main Application Window for managing student records."""
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Student Management System")
        self.root.geometry("900x700")

        # Header Section
        header_frame = ctk.CTkFrame(self.root, fg_color="#4CAF50")
        header_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(header_frame, text="Student Management System", font=("Verdana", 24, "bold"), text_color="white").pack()

        # Input Section
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=10)

        self.create_input_fields()

        # Button Section
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Add Student", command=self.add_student).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Clear Fields", command=self.clear_entries).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Export to CSV", command=self.export_to_csv).grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Show Graph", command=self.show_graph).grid(row=0, column=3, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Manage Attendance", command=self.open_attendance_window).grid(row=1, column=0, columnspan=2, pady=10)
        ctk.CTkButton(button_frame, text="Manage Remarks", command=self.open_remarks_window).grid(row=1, column=2, columnspan=2, pady=10)

        # Treeview for displaying students
        # Treeview Styling
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                background="#2E2E2E",  # Dark background for rows
                foreground="white",  # White text color
                fieldbackground="#2E2E2E",  # Dark background for entry fields
                bordercolor="#2E2E2E",  # Border color to blend with background
                highlightthickness=0)

        style.configure("Treeview.Heading",
                background="#4CAF50",  # Dark green header background
                foreground="white",  # White header text color
                font=("Verdana", 10, "bold"))

        style.map("Treeview", background=[("selected", "#6B8E23")])  # Highlight selected row with olive green

# Treeview Widget
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Age", "Class", "Contact", "Hostel", "Mess"), show="headings")
        for col in ("ID", "Name", "Age", "Class", "Contact", "Hostel", "Mess"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)


        self.display_students()

        self.root.mainloop()

    def create_input_fields(self):
        """Create input fields for student details."""
        self.entry_name = self.create_label_and_entry("Name:", 0)
        self.entry_age = self.create_label_and_entry("Age:", 1)
        self.entry_class = self.create_label_and_entry("Class:", 2)
        self.entry_contact = self.create_label_and_entry("Contact:", 3)
        self.entry_hostel = self.create_label_and_entry("Hostel:", 4)
        self.entry_mess = self.create_label_and_entry("Mess:", 5)

    def create_label_and_entry(self, text, row):
        """Helper to create a label and entry pair."""
        ctk.CTkLabel(self.frame, text=text, font=("Verdana", 12)).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry = ctk.CTkEntry(self.frame, width=250)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    def validate_inputs(self):
        """Validate input fields."""
        if not self.entry_name.get().strip():
            messagebox.showwarning("Input Error", "Name cannot be empty.")
            return False
        if not self.entry_age.get().isdigit():
            messagebox.showwarning("Input Error", "Age must be numeric.")
            return False
        if not self.entry_contact.get().isdigit():
            messagebox.showwarning("Input Error", "Contact must be numeric.")
            return False
        return True

    def add_student(self):
        """Add a new student to the database."""
        if not self.validate_inputs():
            return
        name = self.entry_name.get()
        age = self.entry_age.get()
        student_class = self.entry_class.get()
        contact = self.entry_contact.get()
        hostel = self.entry_hostel.get()
        mess = self.entry_mess.get()

        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, class, contact, hostel, mess) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, age, student_class, contact, hostel, mess))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully!")
        self.clear_entries()
        self.display_students()

    def clear_entries(self):
        """Clear input fields."""
        for entry in (self.entry_name, self.entry_age, self.entry_class, self.entry_contact, self.entry_hostel, self.entry_mess):
            entry.delete(0, ctk.END)

    def display_students(self):
        """Display all students in the Treeview."""
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert('', ctk.END, values=row)
        conn.close()

    def export_to_csv(self):
        """Export student data to a CSV file."""
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        conn.close()

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Age", "Class", "Contact", "Hostel", "Mess"])
                writer.writerows(rows)
            messagebox.showinfo("Export Successful", f"Data exported to {file_path}")

    def show_graph(self):
        """Display a graph of the number of students per hostel."""
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("SELECT hostel, COUNT(*) FROM students GROUP BY hostel")
        data = cursor.fetchall()
        conn.close()
        if data:
            hostels, counts = zip(*data)
            plt.figure(figsize=(8, 6))
            plt.bar(hostels, counts, color="skyblue")
            plt.title("Students per Hostel", fontsize=14)
            plt.xlabel("Hostel")
            plt.ylabel("Number of Students")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showinfo("No Data", "No data available to display!")

    def open_attendance_window(self):
        """Open Attendance Management window."""
        AttendanceWindow(self.root)

    def open_remarks_window(self):
        """Open Remarks Management window."""
        RemarksWindow(self.root)


class AttendanceWindow:
    """Attendance Management Window."""
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Attendance Management")
        self.window.geometry("600x600")
        self.window.attributes("-topmost", True)

        # Bring the window to the front
        self.window.lift()
        self.window.focus_force()

        # Header Section
        header_frame = ctk.CTkFrame(self.window, fg_color="#4CAF50")
        header_frame.pack(fill="x", pady=10)  # Padding handled by pack
        ctk.CTkLabel(header_frame, text="Attendance Management System", font=("Verdana", 22, "bold"), text_color="white").pack()

        # Attendance Section
        frame = ctk.CTkFrame(self.window)  # No padding here
        frame.pack(padx=10, pady=10)  # Padding handled by pack

        # Date input field
        ctk.CTkLabel(frame, text="Enter Date (YYYY-MM-DD):", font=("Verdana", 12)).grid(row=0, column=0, padx=10, pady=5)
        entry_date = ctk.CTkEntry(frame, width=250)
        entry_date.grid(row=0, column=1, padx=10, pady=5)

        def mark_attendance():
            date = entry_date.get().strip()
            if not date:
                messagebox.showwarning("Input Error", "Date is required.")
                return

            # Fetching the students list from the database
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM students")
            students = cursor.fetchall()
            conn.close()

            # Frame for marking attendance
            attendance_form_frame = ctk.CTkFrame(self.window)
            attendance_form_frame.pack(pady=20)

            ctk.CTkLabel(attendance_form_frame, text="Mark Attendance for Each Student", font=("Verdana", 14)).grid(row=0, column=0, columnspan=2)

            student_attendance = {}

            def update_attendance():
                for student_id, var in student_attendance.items():
                    status = "Present" if var.get() else "Absent"
                    conn = sqlite3.connect('students.db')
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                           (student_id, date, status))
                    conn.commit()
                    conn.close()
                messagebox.showinfo("Success", "Attendance marked successfully!")

            row = 1
            for student_id, name in students:
                var = ctk.IntVar()  # Use ctk.IntVar() instead of tk.IntVar()
                ctk.CTkCheckBox(attendance_form_frame, text=name, variable=var).grid(row=row, column=0, sticky="w", padx=10)
                student_attendance[student_id] = var
                row += 1

            ctk.CTkButton(attendance_form_frame, text="Update Attendance", command=update_attendance).grid(row=row, column=0, pady=10)

        ctk.CTkButton(frame, text="Mark Attendance", command=mark_attendance).grid(row=1, column=0, columnspan=2, pady=10)

        def download_attendance():
            date = entry_date.get().strip()
            if not date:
                messagebox.showwarning("Input Error", "Date is required.")
                return

            # Fetch attendance data with the date from the database
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            cursor.execute("""
                SELECT students.name, attendance.status, attendance.date 
                FROM attendance 
                JOIN students ON attendance.student_id = students.id 
                WHERE attendance.date = ?
            """, (date,))
            rows = cursor.fetchall()
            conn.close()

            if not rows:
                messagebox.showinfo("No Data", "No attendance found for this date.")
                return

            # Prompt the user to choose where to save the file
            self.window.attributes("-topmost", False)  # Temporarily allow other dialogs to show above
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            self.window.attributes("-topmost", True)
            
            if file_path:
                # Open the file and write the attendance data including the date
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Name", "Status", "Date"])  # Include Date as a header
                    writer.writerows(rows)

                messagebox.showinfo("Download Successful", f"Attendance data has been downloaded to {file_path}")
        ctk.CTkButton(frame, text="Download Attendance", command=download_attendance).grid(row=2, column=0, columnspan=2, pady=10)

        self.window.mainloop()





class RemarksWindow:
    """Remarks Management Window."""
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Manage Remarks")
        self.window.geometry("600x500")
        self.window.attributes("-topmost", True)
        
        # Header Section
        header_frame = ctk.CTkFrame(self.window, fg_color="#4CAF50")
        header_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(header_frame, text="Manage Remarks", font=("Verdana", 24, "bold"), text_color="white").pack()
        
        # Select Student
        ctk.CTkLabel(self.window, text="Select Student:", font=("Verdana", 12)).pack(pady=10)
        self.student_combobox = ctk.CTkComboBox(self.window, state="readonly", width=250)
        self.student_combobox.pack(pady=5)
        
        self.load_students()

        # Remark Input
        ctk.CTkLabel(self.window, text="Remark:", font=("Verdana", 12)).pack(pady=10)
        self.entry_remark = ctk.CTkEntry(self.window, width=300)
        self.entry_remark.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.window)
        button_frame.pack(pady=10)
        
        ctk.CTkButton(button_frame, text="Add Remark", command=self.add_remark).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="Show Remarks", command=self.display_remarks).grid(row=0, column=1, padx=10)

        # Treeview for Displaying Remarks
        tree_frame = ctk.CTkFrame(self.window)
        tree_frame.pack(fill="both", expand=True, pady=10)
        
        self.remarks_tree = ttk.Treeview(tree_frame, columns=("Remark"), show="headings", height=8)
        self.remarks_tree.heading("Remark", text="Remark")
        self.remarks_tree.pack(fill="both", expand=True)
        
        # Scrollbar for Treeview
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.remarks_tree.yview)
        tree_scroll.pack(side="right", fill="y")
        self.remarks_tree.configure(yscrollcommand=tree_scroll.set)

    def load_students(self):
        """Load students into the combobox."""
        try:
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM students")
            students = cursor.fetchall()
            conn.close()
            self.student_combobox.configure(values=[f"{name} (ID: {id})" for id, name in students])
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading students: {e}")

    def add_remark(self):
        """Add a remark for the selected student."""
        selected_student = self.student_combobox.get()
        remark = self.entry_remark.get().strip()

        if not selected_student or not remark:
            messagebox.showwarning("Input Error", "Please select a student and enter a remark.")
            return

        student_id = selected_student.split(" (ID: ")[1][:-1]
        try:
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO remarks (student_id, remark) VALUES (?, ?)", (student_id, remark))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Remark added successfully!")
            self.entry_remark.delete(0, ctk.END)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error adding remark: {e}")

    def display_remarks(self):
        """Display remarks for the selected student."""
        self.remarks_tree.delete(*self.remarks_tree.get_children())
        selected_student = self.student_combobox.get()

        if not selected_student:
            messagebox.showwarning("Selection Error", "Please select a student to display remarks.")
            return

        student_id = selected_student.split(" (ID: ")[1][:-1]
        try:
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            cursor.execute("SELECT remark FROM remarks WHERE student_id = ?", (student_id,))
            remarks = cursor.fetchall()
            conn.close()

            for remark in remarks:
                self.remarks_tree.insert('', ctk.END, values=remark)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching remarks: {e}")


if __name__ == "__main__":
    DatabaseManager.init_db()
    LoginWindow()
