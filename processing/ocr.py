import pytesseract
from PIL import Image
import os

class OCRRecognizer:
    def __init__(self, tesseract_path: str = None, lang: str = "rus+eng"):
        self.lang = lang
        if tesseract_path and os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    def recognize_from_image(self, image: Image.Image) -> str:
        """Распознать текст из объекта Image"""
        try:
            text = pytesseract.image_to_string(
                image,
                lang=self.lang,
                config='--psm 6 --oem 3'
            )
            return text.strip()
        except Exception as e:
            print(f"❌ OCR ошибка: {e}")
            return ""