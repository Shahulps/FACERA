
import cv2
import face_recognition

def recoglef():
    known_face_encodings= []
    known_face_names= []

    known_person1_image = face_recognition.load_image_file("faces_dataset/person1.jpg")
    known_person2_image =face_recognition.load_image_file("faces_dataset/person2.jpg")
    known_person3_image =face_recognition.load_image_file("faces_dataset/person3.jpg")
    known_person4_image =face_recognition.load_image_file("faces_dataset/person4.jpg")
    known_person5_image =face_recognition.load_image_file("faces_dataset/person5.jpg")
    known_person6_image =face_recognition.load_image_file("faces_dataset/person6.jpg")
    known_person7_image =face_recognition.load_image_file("faces_dataset/person7.jpg")
    known_person8_image =face_recognition.load_image_file("faces_dataset/person8.jpg")
    known_person9_image =face_recognition.load_image_file("faces_dataset/person9.jpg")
    known_person10_image=face_recognition.load_image_file("faces_dataset/person10.jpg")


    known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]
    known_person2_encoding = face_recognition.face_encodings(known_person2_image)[0]
    known_person3_encoding = face_recognition.face_encodings(known_person3_image)[0]
#known_person4_encoding = face_recognition.face_encodings(known_person4_image)[0]
    known_person5_encoding = face_recognition.face_encodings(known_person5_image)[0]
    known_person6_encoding = face_recognition.face_encodings(known_person6_image)[0]
    known_person7_encoding = face_recognition.face_encodings(known_person7_image)[0]
    known_person8_encoding = face_recognition.face_encodings(known_person8_image)[0]
    known_person9_encoding = face_recognition.face_encodings(known_person9_image)[0]
    known_person10_encoding = face_recognition.face_encodings(known_person10_image)[0]


    known_face_encodings.append(known_person1_encoding)
    known_face_encodings.append(known_person2_encoding)
    known_face_encodings.append(known_person3_encoding)
#known_face_encodings.append(known_person4_encoding)
    known_face_encodings.append(known_person5_encoding)
    known_face_encodings.append(known_person6_encoding)
    known_face_encodings.append(known_person7_encoding)
    known_face_encodings.append(known_person8_encoding)
    known_face_encodings.append(known_person9_encoding)
    known_face_encodings.append(known_person10_encoding)




    known_face_names.append("sooraj")
    known_face_names.append(" shahul")
    known_face_names.append("dathan")
        #known_face_names.append("nikhil")
    known_face_names.append("akshay")
    known_face_names.append("arya")
    known_face_names.append("jiffrin")
    known_face_names.append("nikhitha")
    known_face_names.append("pakkaran")
    known_face_names.append("noorjahan")

    video_capture =cv2.VideoCapture (0)

    face_detection_count = 0
    while True:
        ret,frame = video_capture.read()
    
   
        face_locations =face_recognition.face_locations(frame)
        face_encodings =face_recognition.face_encodings(frame,face_locations)
    
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name ="unknown"
        
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            else:
                name="unknown"
            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255),2)
            cv2.putText(frame,name, (left,top - 10), cv2.FONT_HERSHEY_SIMPLEX,1.0, (0,0,255), 2)

        cv2.imshow("Video", frame)
    #face_detection_count -= 1 
    
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            try:
               image_name = f"frmeleft.jpg"
               cv2.imwrite(image_name, frame)
               print(f"Image captured and saved as: {image_name}")
          
            except Exception as e:
                 print(f"Error capturing image: {e}")
    
    
        elif key == ord('q'):  # 'q' key pressed to quit
            break
    video_capture.release()
    cv2.destroyAllWindows()
# done successfully

if __name__ == "__main__":
  recoglef()
            