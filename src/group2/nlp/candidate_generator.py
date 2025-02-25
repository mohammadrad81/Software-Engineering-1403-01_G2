class CandidateGenerator:

    ALPHABET = ['ا', 'آ', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ',
                'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط',
                'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن',
                'و', 'ه', 'ی']

    def generate_deletion_candidates(self, word: str) -> list[str]:
        candidates = []
        for k in range(len(word)):
            begin = word[:k]
            end = word[k + 1:]
            candidate = begin + end
            candidates.append(candidate)
        return candidates

    def generate_insertion_candidates(self, word: str) -> list[str]:
        candidates = []
        for k in range(len(word) + 1):
            for char in CandidateGenerator.ALPHABET:
                begin = word[:k]
                end = word[k:]
                candidate = begin + char + end
                candidates.append(candidate)
        return candidates
    
    def generate_substitution_candidates(self, word) -> list[str]:
        candidates = []
        for i, word_char in enumerate(word):
            for alphabet_char in CandidateGenerator.ALPHABET:
                begin = word[:i]
                end = word[i + 1:]
                candidate = begin + alphabet_char + end
                candidates.append(candidate)
        return candidates
    
    def generate_transposition_candidates(self, word) -> list[str]:
        candidates = []
        for i in range(len(word) - 1):
            temp_word_chars = list(word)
            temp_word_chars[i], temp_word_chars[i + 1] = temp_word_chars[i + 1], temp_word_chars[i] #swap adjacent characters
            candidate = ''.join(temp_word_chars)
            candidates.append(candidate)
        return candidates

    def generate_candidates(self, word: str) -> list[str]:
        candidates = self.generate_deletion_candidates(word)
        candidates += self.generate_insertion_candidates(word)
        candidates += self.generate_substitution_candidates(word)
        candidates += self.generate_transposition_candidates(word)
        return candidates