class SpellChecker:

    def __init__(self,tokenizer, candidate_generator, language_model):
        self.tokenizer = tokenizer
        self.candidate_generator = candidate_generator
        self.language_model = language_model

    def process_text(self, text: str) -> list[tuple[int, int, str, list[str]]]:
        tokens = self.tokenizer.tokenize(text)
        results = []
        for start, end, word in tokens:
            if self.language_model.is_word(word):
                continue
            candidates = self.candidate_generator.generate_candidates(word)
            valid_candidates = [candidate for candidate in candidates if self.language_model.is_word(candidate)]
            sorted_candidates = sorted(valid_candidates, key=lambda x: self.language_model.get_frequency(x), reverse=True)
            top_candidates = sorted_candidates[:min(3, len(sorted_candidates))]
            results.append((start, end, word, top_candidates))

        return results
