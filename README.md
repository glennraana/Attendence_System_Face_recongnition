# Attendance System

Overview

The Attendance System is a Python-based application designed to track employee attendance using facial recognition technology. The system allows for real-time monitoring of check-ins and check-outs, stores attendance data in a MySQL database, and provides an simpel but intuitive GUI for both general users and administrators. The project includes features like capturing user data, checking in and out using facial recognition, and generating attendance reports.

Features

# 1. Facial Recognition Check-In/Out
The system uses a webcam to capture real-time images of users and matches them against a stored database of faces.
Users are automatically checked in when recognized and checked out when leaving.
A time delay is implemented to prevent multiple check-ins/outs within a short time frame.
# 2. Admin Panel
The Admin Panel allows administrators to manage user data, including capturing and storing facial images, names, work card IDs, and company details.
Administrators can easily add new users to the system with the help of a user-friendly GUI.
Users' information and their face encodings are stored securely in the MySQL database.
# 3. Real-Time Dashboard
A dashboard displays currently checked-in users, including their check-in time, name, and work card ID.
The dashboard auto-updates every 30 seconds to ensure real-time monitoring.
# 4. Attendance Reports
The system provides the ability to generate attendance reports, including:
Users who have checked in over the last 24 hours.
Users who have checked in over the last month.
Users who are currently checked in.
# 5. MySQL Database Integration
All user information, face encodings, and attendance logs are stored in a MySQL database.
Secure storage and easy retrieval of user and attendance data.

# Installation

# 1. Clone the Repository

git clone https://github.com/yourusername/attendance-system.git
cd attendance-system
# 2. Install Dependencies
The project uses several Python libraries. You can install them using pip:
tkinter, 
opencv-python, 
Pillow, 
mysql-connector-python, 
face_recognition, 
numpy

# 3. MySQL Setup
Ensure you have MySQL installed and running.
Create a new database for the attendance system.
Update the database.py file with your MySQL credentials.
in Python
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="attendance_system"
)
# 4. Run the Application
You can start the main application and the admin panel by running the respective Python scripts:


python attendance_system.py   # For the attendance check-in/check-out system
python admin_panel.py         # For the admin panel
Usage

# 1. Admin Panel
Open the Admin Panel using admin_panel.py.
Enter the required user information: Name, Work Card ID, Company.
Capture the user's face using the integrated webcam.
Save the data to add the user to the system.
# 2. Attendance System
Open the Attendance System using attendance_system.py.
The system will start detecting faces and check users in or out based on recognition.
The dashboard will display the currently checked-in users.
# 3. Generating Reports
Use the buttons on the right side of the dashboard to generate and print attendance reports for the last 24 hours, the last month, or the currently checked-in users.
Project Structure


attendance-system/
│
├── admin_panel.py             # Admin Panel GUI for managing users
├── attendance_system.py        # Main attendance system with facial recognition
├── dashboard.py                # Dashboard GUI for displaying checked-in users
├── database.py                 # MySQL database interaction functions
├── requirements.txt            # List of required Python packages
└── README.md                   # This README file
Future Improvements

Multi-Camera Support: Add support for multiple cameras to monitor different entrances.
Remote Access: Implement a web-based dashboard for remote access to attendance data.
Enhanced Security: Improve security features, including encryption for sensitive data.
Mobile App Integration: Develop a mobile app for users to check their attendance status and history.
Contribution

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss potential improvements.
The backend has been the main goal for me here. tie everything together in a good way so the design have not been a focus for this project. 
I wanted to do a project totaly by my self and without Kaggle or othe platforms so this was a very cool project to work on. 
I have used ChatGPT alot and and google even more, but that is part of the life. 

Please feel free to contact me @ glennraana@gmail.com if any thoughts about project. 

