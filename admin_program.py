import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import mysql.connector
import face_recognition

class AdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registrer Ny Bruker")

        self.captured_frame = None

        # Configure grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)

        # Video capture
        self.cap = cv2.VideoCapture(0)
        self.video_frame = tk.Label(root)
        self.video_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Right panel frame
        self.right_panel = tk.Frame(root, bg="black", padx=20, pady=20)
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        # Checkbox for valid work card
        self.valid_card_var = tk.IntVar()
        self.valid_card_check = tk.Checkbutton(self.right_panel, text="Gyldig HMS-Kort", variable=self.valid_card_var, bg="black")
        self.valid_card_check.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Name entry
        self.name_label = tk.Label(self.right_panel, text="Navn:", bg="black")
        self.name_label.grid(row=1, column=0, sticky="w")
        self.name_entry = tk.Entry(self.right_panel)
        self.name_entry.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        # Work card ID entry
        self.work_id_label = tk.Label(self.right_panel, text="HMS-KORT Nummer:", bg="black")
        self.work_id_label.grid(row=3, column=0, sticky="w")
        self.work_id_entry = tk.Entry(self.right_panel)
        self.work_id_entry.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        # Company entry
        self.company_label = tk.Label(self.right_panel, text="Firma:", bg="black")
        self.company_label.grid(row=5, column=0, sticky="w")
        self.company_entry = tk.Entry(self.right_panel)
        self.company_entry.grid(row=6, column=0, sticky="ew", pady=(0, 20))

        # Take Picture and Save Button
        self.take_picture_and_save_button = tk.Button(self.right_panel, text="Ta bilde og lagre", command=self.capture_and_save)
        self.take_picture_and_save_button.grid(row=7, column=0, sticky="ew")

        # Continuously update the video frame
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_frame.imgtk = imgtk
            self.video_frame.configure(image=imgtk)

        self.root.after(10, self.update_frame)

    def capture_and_save(self):
        ret, frame = self.cap.read()
        if ret:
            self.captured_frame = frame  
            cv2.imshow("Captured Image", frame)

            # Extract face encoding from the captured frame
            face_locations = face_recognition.face_locations(frame)
            if face_locations:
                face_encodings = face_recognition.face_encodings(frame, face_locations)
                face_encoding = face_encodings[0]  # Assuming one face

                encoding_blob = face_encoding.tobytes()

                name = self.name_entry.get()
                work_card_id = self.work_id_entry.get()
                company = self.company_entry.get()
                has_valid_card = self.valid_card_var.get()
                image = cv2.imencode('.jpg', frame)[1].tobytes()

                if not name or not work_card_id or not company:
                    messagebox.showerror("Error", "All fields are required!")
                    return

                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="HKtcc301276",
                    database="attendance_system"
                )
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (name, work_card_id, company, image, face_encoding, has_valid_card) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (name, work_card_id, company, image, encoding_blob, has_valid_card))
                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Data saved successfully!")
                self.clear_entries()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.work_id_entry.delete(0, tk.END)
        self.company_entry.delete(0, tk.END)

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminApp(root)
    root.mainloop()





