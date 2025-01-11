import json
import os

class OneGramLanguageModel:
    def __init__(self,
                 data: dict[str, int]=None,
                 file_path: str="./src/group2/data/cleaned_onegram_lm.json"):
        if data is None:
            with open(file_path, 'r') as f:
                self.data = json.load(f)
        else:
            self.data=data
    
    def is_word(self, word: str) -> bool:
        return word in self.data.keys()
    
    def get_frequency(self, word: str) -> int:
        return self.data.get(word, 0)