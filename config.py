import os

# Настройки Tesseract
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if not os.path.exists(TESSERACT_PATH):
    TESSERACT_PATH = None  # будет искать в PATH

# База данных
DB_URL = "sqlite:///memes.db"

# Папка с изображениями
IMAGES_DIR = "data/images"

# Язык OCR
OCR_LANG = "rus+eng"