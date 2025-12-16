from PIL import Image, ImageEnhance, ImageOps

class ImagePreprocessor:
    def preprocess(self, image_path: str) -> Image.Image:
        """Обработать изображение и вернуть PIL.Image"""
        try:
            image = Image.open(image_path)
            gray = image.convert('L')
            inverted = ImageOps.invert(gray)
            enhanced = ImageEnhance.Contrast(inverted).enhance(2.0)
            return enhanced
        except Exception as e:
            print(f"⚠️  Ошибка препроцессинга: {e}")
            # Fallback
            return Image.open(image_path).convert('L')