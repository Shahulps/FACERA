import cv2
import os
import time

def capture_image():
  """Captures an image from the webcam when Enter is pressed and saves it to the 'data' directory with a unique filename. Displays the number of captured images on the frame."""

  # Create 'data' directory if it doesn't exist
  data_dir = "data"
  if not os.path.exists(data_dir):
    os.makedirs(data_dir)

  cam = cv2.VideoCapture(0)  # Open webcam
  num_captured_images = 0  # Initialize counter for captured images

  while True:
    result, image = cam.read()  # Capture frame

    if not result:
      print("Error: Unable to capture image from webcam.")
      break

    # Display the number of captured images on the frame
    font = cv2.FONT_HERSHEY_SIMPLEX  # Font for text
    text = f"Images Captured: {num_captured_images}"
    text1=f"press q for quit"
    cv2.putText(image, text, (10, 20), font, 0.7, (255, 255, 0), 2)# Text placement, color, and thickness
    cv2.putText(image, text1, (10, 420), font, 0.7, (255, 0, 0), 2)
    cv2.imshow("FACEERA", image)

    # Check for Enter key press
    key = cv2.waitKey(1) & 0xFF  # Wait for a key press with bitwise AND

    if key == 13:  # Enter key pressed
      # Generate unique filename with timestamp
      timestamp = int(time.time())
      filename = f"{data_dir}/image_{timestamp}.jpg"

      # Save image
      try:
        cv2.imwrite(filename, image)
        print(f"Image saved successfully to '{filename}'.")
        num_captured_images += 1  # Increment counter after successful capture
      except Exception as e:
        print(f"Error saving image: {e}")

    elif key == ord('q'):  # 'q' key pressed to quit
      break

  cam.release()
  cv2.destroyAllWindows()

if __name__ == "__main__":
  capture_image()
