import cv2
import os  # For file path validation

def generate_dataset():
    face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            return None

        # Only call face_cropped once per frame if needed for both saving and displaying
        cropped_face = img[faces[0][0]:faces[0][0] + faces[0][2],
                           faces[0][1]:faces[0][1] + faces[0][3]]
        return cropped_face

    cap = cv2.VideoCapture(0)  # Change to 1 if using a secondary camera

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Initialize ID outside the loop for incrementing across runs
    id = input("Enter a unique ID for this dataset collection: ")
    img_id = 0

    print("Press Enter to capture a sample, or Esc to exit after capturing 5 samples.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame from camera.")
            break

        cropped_face = face_cropped(frame)
        if cropped_face is not None:
            img_id += 1

            # Create data directory if it doesn't exist
            data_dir = "data/"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            face = cv2.resize(cropped_face, (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            file_name_path = os.path.join(data_dir, "user." + str(id) + "." + str(img_id) + ".jpg")
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("Cropped face", face)

            if cv2.waitKey(1) == 13 or img_id == 5:  # Enter key or capture 5 samples
                break

    cap.release()
    cv2.destroyAllWindows()
    print("Dataset collection completed!")

if __name__ == "__main__":
    generate_dataset()
