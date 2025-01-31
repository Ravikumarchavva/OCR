class Invoice:
    def __init__(self, data):
        self.data = data
    
    def __getitem__(self, key):
        return self.data.get(key, None)
