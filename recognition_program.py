import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
from database import update_checkout, get_last_attendance, log_attendance, get_user_by_face
from datetime import datetime, timedelta
import numpy as np

class RecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trollkom Adgangsystem")

        # Configure the grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=4)  # Make the right panel larger

        # Set up the smaller video frame on the left
        self.video_frame = tk.Label(root, width=600, height=400)  # Set specific dimensions
        self.video_frame.grid(row=0, column=0, padx=10, pady=10)

        # Larger right-side panel for status and checkmark
        self.status_frame = tk.Frame(root, bg="black", width=600, height=480)
        self.status_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Status label (text)
        self.status_label = tk.Label(self.status_frame, text="Ansikts gjenkjenning pågår....", font=('Helvetica', 14), bg="black")
        self.status_label.pack(pady=20)

        # Checkmark label (image)
        self.checkmark_label = tk.Label(self.status_frame, bg="black")
        self.checkmark_label.pack(pady=20)

        self.cap = cv2.VideoCapture(0)
        self.last_action_time = None  # Initialize the last action time

        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_frame.imgtk = imgtk
            self.video_frame.configure(image=imgtk)

            if self.last_action_time is None or datetime.now() >= self.last_action_time:
                face_locations = face_recognition.face_locations(frame)
                if face_locations:
                    face_encodings = face_recognition.face_encodings(frame, face_locations)
                    if face_encodings:
                        face_encoding = face_encodings[0]
                        user = get_user_by_face(face_encoding)
                        if user:
                            last_attendance = get_last_attendance(user['id'])
                            if last_attendance and not last_attendance['check_out_time']:
                                update_checkout(last_attendance['id'])
                                self.update_status(user['name'], checked_in=False)
                            else:
                                work_card_id = user.get('work_card_id', None)
                                log_attendance(user['id'], user['name'], work_card_id)
                                self.update_status(user['name'], checked_in=True)
                            
                            self.last_action_time = datetime.now() + timedelta(seconds=20)
                        else:
                            self.status_label.config(text="Ansikt er ikke gjenkjent, eller HMS-kort er ikke gyldig. Kontakt nærmeste leder.")

        self.root.after(10, self.update_frame)

    def update_status(self, name, checked_in):
        if checked_in:
            checkmark_img = Image.open("/Users/glenn/Cheek_in_system/Eo_circle_green_checkmark.svg.png")  # Load your green checkmark image
            self.status_label.config(text=f"{name} \nHar sjekket inn\nHMS-Kort er gyldig", fg="green", font=('Helvetica', 20, 'bold'))
        else:
            checkmark_img = Image.open("/Users/glenn/Cheek_in_system/aa0e46ec506bbc88ebbb4d86eb64a20a.png")  # Load your red checkmark image
            self.status_label.config(text=f"{name}\nEr sjekket ut.", fg="red", font=('Helvetica', 20, 'bold'))

        checkmark_img = checkmark_img.resize((100, 100), Image.Resampling.LANCZOS)
        imgtk = ImageTk.PhotoImage(checkmark_img)
        self.checkmark_label.imgtk = imgtk
        self.checkmark_label.configure(image=imgtk)

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = RecognitionApp(root)
    root.mainloop()
