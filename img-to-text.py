import pytesseract
from PIL import Image
import cv2
import numpy as np
import easyocr

def increase_resolution(image):
    scale_factor = 1.5
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
    return resized_image

def enhance_contrast_and_denoise(image):
    denoised_image = cv2.fastNlMeansDenoising(image, h=30)
    contrast_image = cv2.convertScaleAbs(denoised_image, alpha=1.5, beta=0)
    return contrast_image

def adaptive_threshold(image):
    adaptive_thresh = cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )
    return adaptive_thresh

def preprocess_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Check if the image is loaded successfully
    if image is None:
        raise FileNotFoundError(f"Error: Unable to load image at {image_path}")

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Preprocessing Steps
    resized_image = increase_resolution(gray_image)
    enhanced_image = enhance_contrast_and_denoise(resized_image)
    processed_image = adaptive_threshold(enhanced_image)

    return processed_image

def read_text_with_tesseract(image_path):
    # Preprocess the image
    processed_image = preprocess_image(image_path)

    # Use pytesseract to extract text
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(processed_image, lang='eng', config=custom_config)

    return text

def read_text_with_easyocr(image_path):
    reader = easyocr.Reader(['en'], gpu=False)  # Disable GPU if not available
    results = reader.readtext(image_path)

    text = ''
    for result in results:
        text += result[1] + '\n'

    return text

if __name__ == "__main__":
    # Path to the image file
    image_path = 'img1.png'

    try:
        # Read text using Tesseract
        tesseract_text = read_text_with_tesseract(image_path)
        print("Extracted Text from Image using Tesseract:")
        print(tesseract_text)

        # Read text using EasyOCR
        easyocr_text = read_text_with_easyocr(image_path)
        print("\nExtracted Text from Image using EasyOCR:")
        print(easyocr_text)

    except FileNotFoundError as e:
        print(str(e))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
