import cv2
import pytesseract

class ExtractText:
    @staticmethod
    def extract_text_from_image(image_path):
        image = cv2.imread(image_path)
        extract_text = pytesseract.image_to_string(image)
        return extract_text
