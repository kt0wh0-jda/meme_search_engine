from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Text

Base = declarative_base()

class MemeModel(Base):
    __tablename__ = "memes"
    id = Column(Integer, primary_key=True)
    image_path = Column(Text, nullable=False)
    ocr_text_raw = Column(Text, nullable=False)
    ocr_text_clean = Column(Text, nullable=False)