import mysql.connector
from datetime import datetime
import numpy as np
import face_recognition

def get_last_attendance(user_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xxxxxxxxx",
        database="attendance_system"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM attendance_system.attendance_log 
        WHERE user_id = %s 
        ORDER BY check_in_time DESC 
        LIMIT 1
    """, (user_id,))
    last_attendance = cursor.fetchone()
    cursor.close()
    conn.close()
    return last_attendance

def update_checkout(attendance_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="HKtcc301276",
        database="attendance_system"
    )
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE attendance_system.attendance_log 
        SET check_out_time = %s 
        WHERE id = %s
    """, (datetime.now(), attendance_id))
    conn.commit()
    cursor.close()
    conn.close()

def log_attendance(user_id, name, work_card_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="HKtcc301276",
        database="attendance_system"
    )
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO attendance_system.attendance_log (user_id, check_in_time, name, work_card_id) 
        VALUES (%s, %s, %s, %s)
    """, (user_id, datetime.now(), name, work_card_id))
    conn.commit()
    cursor.close()
    conn.close()


def get_user_by_face(face_encoding):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xxxxxxx",
        database="attendance_system"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, face_encoding, work_card_id FROM users")
    users = cursor.fetchall()
    
    for user in users:
        if user['face_encoding']:
            known_face_encoding = np.frombuffer(user['face_encoding'], dtype=np.float64)
            matches = face_recognition.compare_faces([known_face_encoding], face_encoding)
            if matches[0]:
                cursor.close()
                conn.close()
                return user
    
    cursor.close()
    conn.close()
    return None


