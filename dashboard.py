import tkinter as tk
from tkinter import ttk
import mysql.connector
from datetime import datetime, timedelta

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Dashboard")
        self.root.configure(bg='black')

        self.setup_ui()
        self.update_dashboard()

    def setup_ui(self):
        # Add a heading
        heading_label = tk.Label(self.root, text="Innsjekket på anlegg", font=('Helvetica', 24, 'bold'), bg='black', fg='white')
        heading_label.grid(row=0, column=0, columnspan=3, pady=20)

        # Treeview with larger text
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 16, 'bold'), background='black', foreground='black')
        style.configure("Treeview", font=('Helvetica', 14))

        self.tree = ttk.Treeview(self.root, columns=('Name', 'Work Card ID', 'Check-in Time'), show='headings', height=10)
        self.tree.heading('Name', text='Navn')
        self.tree.heading('Work Card ID', text='HMS-KORT ID')
        self.tree.heading('Check-in Time', text='Innsjekket tid')
        self.tree.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')

        # Button panel on the right side
        button_frame = tk.Frame(self.root, bg='gray', padx=10, pady=10)
        button_frame.grid(row=1, column=2, sticky='ns', padx=20, pady=10)

        button_font = ('Helvetica', 14, 'bold')

        # Buttons with images (assuming you have the images in the correct path)
        print_24h_button = tk.Button(button_frame, text="Raport siste 24 timer", font=button_font, command=self.print_last_24_hours, bg='lightgray')
        print_24h_button.pack(pady=10, fill=tk.X)

        print_month_button = tk.Button(button_frame, text="Rapport Siste mnd.", font=button_font, command=self.print_last_month, bg='lightgray')
        print_month_button.pack(pady=10, fill=tk.X)

        print_checked_in_button = tk.Button(button_frame, text="Rapport Innsjekket akkurat nå", font=button_font, command=self.print_checked_in_now, bg='lightgray')
        print_checked_in_button.pack(pady=10, fill=tk.X)

    def update_dashboard(self):
        # Clear the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Connect to the database and retrieve data
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="HKtcc301276",
            database="attendance_system"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT users.name, users.work_card_id, attendance_log.check_in_time
            FROM attendance_log
            JOIN users ON attendance_log.user_id = users.id
            WHERE attendance_log.check_out_time IS NULL
        """)

        rows = cursor.fetchall()

        # Insert data into the treeview
        for row in rows:
            self.tree.insert('', tk.END, values=row)

        cursor.close()
        conn.close()

        # Refresh the dashboard every 30 seconds
        self.root.after(30000, self.update_dashboard)

    def print_last_24_hours(self):
        # Logic to print attendance of last 24 hours
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="HKtcc301276",
            database="attendance_system"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT users.name, users.work_card_id, attendance_log.check_in_time, attendance_log.check_out_time
            FROM attendance_log
            JOIN users ON attendance_log.user_id = users.id
            WHERE attendance_log.check_in_time >= %s
        """, (datetime.now() - timedelta(days=1),))

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        print("Attendance Last 24 Hours:")
        for row in rows:
            print(row)

    def print_last_month(self):
        # Logic to print attendance of last month
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="HKtcc301276",
            database="attendance_system"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT users.name, users.work_card_id, attendance_log.check_in_time, attendance_log.check_out_time
            FROM attendance_log
            JOIN users ON attendance_log.user_id = users.id
            WHERE attendance_log.check_in_time >= %s
        """, (datetime.now() - timedelta(days=30),))

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        print("Attendance Last Month:")
        for row in rows:
            print(row)

    def print_checked_in_now(self):
        # Logic to print currently checked-in people
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="HKtcc301276",
            database="attendance_system"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT users.name, users.work_card_id, attendance_log.check_in_time
            FROM attendance_log
            JOIN users ON attendance_log.user_id = users.id
            WHERE attendance_log.check_out_time IS NULL
        """)

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        print("Currently Checked-in People:")
        for row in rows:
            print(row)

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()


