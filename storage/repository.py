from sqlalchemy.orm import Session
from domain.meme import Meme
from storage.models import MemeModel
from storage.database import SessionLocal
import os

class MemeRepository:
    def __init__(self):
        self.session: Session = SessionLocal()
    
    def add(self, meme: Meme) -> None:
        # Проверяем, нет ли уже такого файла
        existing = self.session.query(MemeModel)\
            .filter(MemeModel.image_path == meme.image_path)\
            .first()
        
        if existing:
            print(f"⚠️  Файл уже в БД: {os.path.basename(meme.image_path)}")
            return  # не добавляем дубликат
        
        db_meme = MemeModel(
            image_path=meme.image_path,
            ocr_text_raw=meme.ocr_text_raw,
            ocr_text_clean=meme.ocr_text_clean
        )
        self.session.add(db_meme)
        self.session.commit()
    
    def get_all(self, limit: int = 500) -> list[Meme]:
        """Получить все мемы"""
        db_memes = self.session.query(MemeModel).limit(limit).all()
        return [
            Meme(
                id=m.id,
                image_path=m.image_path,
                ocr_text_raw=m.ocr_text_raw,
                ocr_text_clean=m.ocr_text_clean
            )
            for m in db_memes
        ]
    
    def __del__(self):
        """Закрыть сессию при удалении объекта"""
        self.session.close()