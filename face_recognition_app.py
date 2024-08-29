import face_recognition
import cv2

def extract_face_encoding(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_image)
    return encodings[0] if encodings else None

def is_face_match(known_encoding, face_encoding):
    return face_recognition.compare_faces([known_encoding], face_encoding)[0]
