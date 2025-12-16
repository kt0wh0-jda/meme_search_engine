from dataclasses import dataclass
from typing import Optional

@dataclass
class Meme:
    id: Optional[int]
    image_path: str
    ocr_text_raw: str
    ocr_text_clean: str