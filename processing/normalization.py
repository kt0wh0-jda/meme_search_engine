class TextNormalizer:
    def normalize(self, text: str) -> str:
        if not text:
            return ""
        # Простая нормализация
        return text.lower().strip()