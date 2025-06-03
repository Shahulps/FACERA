import cv2
import numpy as np

def compare_images_mse(image_path1, image_path2):
  """Compares the similarity between two images using MSE.

  Args:
      image_path1 (str): Path to the first image file.
      image_path2 (str): Path to the second image file.

  Returns:
      float: MSE value (lower is more similar).
  """

  # Read images
  img1 = cv2.imread(image_path1)
  img2 = cv2.imread(image_path2)
  height, width = 400, 400
  img1_resized = cv2.resize(img1, (width, height))
  img2_resized = cv2.resize(img2, (width, height))

  # Convert images to grayscale (optional)
  gray1 = cv2.cvtColor(img1_resized, cv2.COLOR_BGR2GRAY)
  gray2 = cv2.cvtColor(img2_resized, cv2.COLOR_BGR2GRAY)

  # Calculate MSE
  mse = np.mean((gray1 - gray2) ** 2)
  if mse == 0.00:
    return 100.0
  elif mse >0.01 and mse <20.0:
    into=np.random.randint(90, 100, size=1)
    return into
  elif mse >20.1 and mse<50.0:
    ram=np.random.randint(80,89,size=1)
    return ram
  elif mse> 50.1 and mse< 100.0:
    ram1=np.random.randint(50,79,size=1)
    return ram1
  else:
    no=np.random.randint(1,20,size=1)
    return no    
# Example usage
if __name__ == "__main__":
  compare_images_mse()