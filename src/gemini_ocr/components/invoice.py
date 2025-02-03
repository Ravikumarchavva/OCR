class Invoice:
    def __init__(self, data):
        self.data = data
    
    def __getitem__(self, key):
        '''Returns the value of the key from the data dictionary.'''
        return self.data.get(key, None)
