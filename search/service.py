from storage.repository import MemeRepository
from search.engine import SearchEngine

class SearchService:
    def __init__(self, repo: MemeRepository, engine: SearchEngine):
        self.repo = repo
        self.engine = engine
    
    def search(self, query: str):
        memes = self.repo.get_all()
        return self.engine.rank(memes, query)