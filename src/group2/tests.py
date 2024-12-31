from django.test import TestCase
from .tokenizer import PositionalTokenizer
from .candidate_generator import CandidateGenerator
from .language_model import OneGramLanguageModel

# Create your tests here.
class PositionalTokenizerTestCase(TestCase):

    def test_empty_text(self):
        tokenizer = PositionalTokenizer()
        text = ""
        tokens = tokenizer.tokenize(text)
        self.assertEqual(tokens, [], msg="tokenized empty text must be an empty list!")
    
    def test_single_word_text(self):
        tokenizer = PositionalTokenizer()
        text = "ریش"
        tokens = tokenizer.tokenize(text)
        expected_result = [(0, 3, "ریش")]
        self.assertEqual(tokens, expected_result, msg="tokenized single word text must contain a tuple of (0, len(text), word)!")

    def test_multi_word_text(self):
        tokenizer = PositionalTokenizer()
        text = "ریش سفیدان"
        tokens = tokenizer.tokenize(text)
        expected_result = [
            (0, 3, "ریش"),
            (4, 10, "سفیدان")
        ]
        self.assertEqual(tokens, expected_result)


class CandidateGeneratorTestCase(TestCase):

    def test_empty_text_deletion_candidates(self):
        candidate_generator = CandidateGenerator()
        text = ""
        candidates = candidate_generator.generate_deletion_candidates(text)
        self.assertEqual(candidates, [], "No deletion candidates should be generated for empty text!")
    
    def test_empty_text_substitution_candidates(self):
        candidate_generator = CandidateGenerator()
        text = ""
        candidates = candidate_generator.generate_substitution_candidates(text)
        self.assertEqual(candidates, [], "No substitution candidates should be generated for empty text!")
    
    def test_empty_text_transposition_candidates(self):
        candidate_generator = CandidateGenerator()
        text = ""
        candidates = candidate_generator.generate_transposition_candidates(text)
        self.assertEqual(candidates, [], "No transposition candidates should be generated for empty text!")

    def test_empty_text_insertion_candidates(self):
        candidate_generator = CandidateGenerator()
        text = ""
        candidates = candidate_generator.generate_insertion_candidates(text)
        self.assertEqual(candidates,
                         candidate_generator.ALPHABET,
                         "#Alphabet insertion candidates should be generated for empty text!")
    
    def test_empty_text_candidates(self):
        candidate_generator = CandidateGenerator()
        text = ""
        candidates = candidate_generator.generate_candidates(text)
        self.assertEqual(candidates,
                         candidate_generator.ALPHABET,
                         "#Alphabet candidates should be generated for empty text (just for insertion)!")
    
    def test_deletion_candidates(self):
        candidate_generator = CandidateGenerator()
        text = "ریش"
        candidates = set(candidate_generator.generate_deletion_candidates(text))
        expected_result = {"ری", "رش", "یش"}
        self.assertEqual(candidates, expected_result, "Wrong deletion candidates!\n"+
                                                      f"text: {text}\n" +
                                                      f"expected: {expected_result}\n" +
                                                      f"generated: {candidates}\n")
    
    def test_transposition_candidates(self):
        candidate_generator = CandidateGenerator()
        text = "ریش"
        candidates = set(candidate_generator.generate_transposition_candidates(text))
        expected_result = {"یرش", "رشی"}
        self.assertEqual(candidates, expected_result, "Wrong deletion candidates!\n"+
                                                      f"text: {text}\n" +
                                                      f"expected: {expected_result}\n" +
                                                      f"generated: {candidates}\n")
        

class OneGramLanguageModelTestCase(TestCase):

    def test_is_word(self):
        language_model = OneGramLanguageModel()
        self.assertTrue(language_model.is_word("غزال"))
        self.assertTrue(language_model.is_word("کیمیا"))
        self.assertTrue(language_model.is_word("محمد"))
        self.assertTrue(language_model.is_word("قسطنطنیه"))
        self.assertTrue(language_model.is_word("سلام"))
        self.assertFalse(language_model.is_word("سلامز"))

    def test_frequency(self):
        language_model = OneGramLanguageModel()
        self.assertGreater(language_model.get_frequency("سلام"), language_model.get_frequency("سلامز"))
        self.assertEqual(language_model.get_frequency("سلامز"), 0)