class DDGS:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    def text(self, query, region=None, max_results=1):
        # return empty results
        return []
