import os
from config import IMAGES_DIR, TESSERACT_PATH, OCR_LANG
from domain.meme import Meme
from processing.ocr import OCRRecognizer
from processing.preprocessing import ImagePreprocessor
from processing.normalization import TextNormalizer
from storage.repository import MemeRepository
from search.levenshtein import LevenshteinSearchEngine
from search.service import SearchService

def main():
    print("=" * 50)
    print("🤖 Meme Search MVP")
    print("=" * 50)
    
    # 1. Инициализация
    preprocessor = ImagePreprocessor()
    ocr = OCRRecognizer(TESSERACT_PATH, OCR_LANG)
    normalizer = TextNormalizer()
    repo = MemeRepository()
    
    # 2. Создание БД
    from storage.models import Base
    from storage.database import engine
    
    import os
    
    Base.metadata.create_all(bind=engine)
    print("✅ Создана новая БД")
    
    # 3. Обработка изображений
    image_files = []
    if os.path.exists(IMAGES_DIR):
        for file in os.listdir(IMAGES_DIR):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                path = os.path.join(IMAGES_DIR, file)
                if os.path.exists(path):
                    image_files.append((file, path))
    
    print(f"\n📁 Найдено изображений: {len(image_files)}")
    
    for filename, filepath in image_files:
        print(f"\n📄 Обработка: {filename}")
        
        try:
            # Препроцессинг
            processed_image = preprocessor.preprocess(filepath)
            
            # OCR
            raw_text = ocr.recognize_from_image(processed_image)
            
            # Нормализация
            clean_text = normalizer.normalize(raw_text)
            
            # Сохранение
            meme = Meme(
                id=None,
                image_path=filepath,
                ocr_text_raw=raw_text,
                ocr_text_clean=clean_text
            )
            repo.add(meme)
            
            if clean_text:
                print(f"  ✅ Текст: '{clean_text[:60]}...'")
            else:
                print(f"  ⚠️  Текст не распознан")
                
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
    
    # 4. ТЕСТИРОВАНИЕ ПОИСКА
    print("\n" + "=" * 50)
    print("🔍 ТЕСТИРОВАНИЕ ПОИСКА")
    print("=" * 50)
    
    # Получаем все мемы
    all_memes = repo.get_all()
    print(f"📊 В базе: {len(all_memes)} уникальных мемов")
    
    # Создаем поисковый движок
    search_engine = LevenshteinSearchEngine()
    search_service = SearchService(repo, search_engine)
    
    # Тестовые запросы (основанные на реальных текстах из ваших мемов)
    test_queries = [
        "когда",        # из "Когда случайно нажимаешь"
        "когда случайно нажал",     # из "Когда случайно нажимаешь"  
        "кто плавает там",      # из "кто там плавает"
        "спасибо включающим фильмы",     # из "бокал 38 учителей"
        "привет",       # общий тест
        "мем",          # общий тест
    ]
    
    for query in test_queries:
        print(f"\n🔎 Запрос: '{query}'")
        results = search_service.search(query)
        
        print(f"   Найдено: {len(results)}")
        
        # Показываем топ-3
        for i, result in enumerate(results[:3], 1):
            filename = os.path.basename(result.meme.image_path)
            text_preview = result.meme.ocr_text_clean[:50] + "..." if result.meme.ocr_text_clean else ""
            print(f"   {i}. 📊 {result.score:.3f} | 📄 {filename}")
            if text_preview:
                print(f"      '{text_preview}'")
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено!")

if __name__ == "__main__":
    main()