import cv2
import numpy as np

def compare_faces(image1, image2):
  """
  Compares faces in two images and returns a similarity score.

  Args:
      image1: The first image (BGR format).
      image2: The second image (BGR format).

  Returns:
      A string containing the similarity score (0-100%) or None if no faces are detected.
  """

  # Face detection using Haar cascade classifier (replace if needed)
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

  # Convert images to grayscale
  gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
  gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

  # Detect faces
  faces1 = face_cascade.detectMultiScale(gray1, 1.1, 4)
  faces2 = face_cascade.detectMultiScale(gray2, 1.1, 4)

  # Check for single face detection in each image
  if len(faces1) == 1 and len(faces2) == 1:
    (x1, y1, w1, h1) = faces1[0]
    (x2, y2, w2, h2) = faces2[0]

    # Extract ROIs
    face1_roi = gray1[y1:y1+h1, x1:x1+w1]
    face2_roi = gray2[y2:y2+h2, x2:x2+w2]

    # Print shapes for verification
    print(f"Face 1 ROI shape: {face1_roi.shape}")
    print(f"Face 2 ROI shape: {face2_roi.shape}")

    # Ensure both ROIs are grayscale (assuming grayscale input)
    
    # Resize ROIs to a fixed size while maintaining aspect ratio
    target_size = (100, 100)  # Adjust target size as needed
    face1_roi = cv2.resize(face1_roi, dsize=target_size, interpolation=cv2.INTER_AREA)
    face2_roi = cv2.resize(face2_roi, dsize=target_size, interpolation=cv2.INTER_AREA)

    # Feature extraction using pixel-wise difference (consider alternatives)
    diff = cv2.absdiff(face1_roi, face2_roi)
    diff_norm = cv2.norm(diff)
    # Calculate normalized Euclidean distance
    euclidean_distance = np.linalg.norm(diff.flatten()) / np.sqrt(diff.size)
    similarity = 1 - (diff_norm / (np.sqrt(diff.size) * 255))

    # Similarity interpretation (adjust based on your needs)
    similarity_score = 100 * similarity  # Higher score for smaller distance

    return f" {similarity_score:.2f}%"
  else:
    print("Error: No or multiple faces detected")
    return None

# Example usage
'''image1 = cv2.imread('faces_dataset/person1.jpg')
image2 = cv2.imread('faces_dataset/person1.jpg')
similarity_message = compare_faces(image1, image2)
if similarity_message:
  print(similarity_message)
else:
  print("Error occurred during face comparison.")'''
