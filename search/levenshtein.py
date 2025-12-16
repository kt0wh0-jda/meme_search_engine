# search/levenshtein.py
from search.engine import SearchEngine, SearchResult

class LevenshteinSearchEngine(SearchEngine):
    def rank(self, memes, query: str) -> list[SearchResult]:
        if not query or not query.strip():
            return []
        
        query_lower = query.lower().strip()
        results = []
        
        for meme in memes:
            # Пропускаем мемы без текста
            if not meme.ocr_text_clean:
                continue
                
            # Вычисляем сходство
            similarity = self._calculate_similarity(
                query_lower, 
                meme.ocr_text_clean.lower()
            )
            
            # Добавляем только если есть сходство
            if similarity > 0:
                results.append(SearchResult(meme, similarity))
        
        # Сортируем по убыванию сходства
        return sorted(results, key=lambda x: x.score, reverse=True)
    
    def _calculate_similarity(self, query: str, text: str) -> float:
        """
        Вычисляет сходство на основе расстояния Левенштейна
        """
        if not query or not text:
            return 0.0
        
        # Если запрос полностью содержится в тексте
        if query in text:
            return 1.0
        
        # Или текст в запросе
        if text in query:
            return 0.8
        
        # Разбиваем на слова для частичного совпадения
        query_words = set(query.split())
        text_words = set(text.split())
        
        # Есть ли общие слова?
        common_words = query_words.intersection(text_words)
        if common_words:
            return len(common_words) / len(query_words)
        
        # Иначе используем расстояние Левенштейна
        distance = self._levenshtein_distance(query, text[:len(query)*2])
        max_len = max(len(query), len(text[:len(query)*2]))
        
        if max_len == 0:
            return 0.0
        
        # Преобразуем расстояние в сходство (0-1)
        similarity = 1.0 - (distance / max_len)
        return max(0.0, similarity)  # не меньше 0
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Реализация расстояния Левенштейна"""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]