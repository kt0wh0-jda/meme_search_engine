from domain.meme import Meme

class SearchResult:
    def __init__(self, meme: Meme, score: float):
        self.meme = meme
        self.score = score

class SearchEngine:
    def rank(self, memes: list[Meme], query: str) -> list[SearchResult]:
        raise NotImplementedError