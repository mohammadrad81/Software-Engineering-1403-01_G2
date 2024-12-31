from django.test import TestCase
from .tokenizer import PositionalTokenizer

# Create your tests here.
class PositionalTokenizerTestCase(TestCase):

    def test_empty_text(self):
        tokenizer = PositionalTokenizer()
        text = ""
        tokens = tokenizer.tokenize(text)
        self.assertEqual(tokens, [], msg="tokenized empty text must be an empty list")
    
    def test_single_word_text(self):
        tokenizer = PositionalTokenizer()
        text = "ریش"
        tokens = tokenizer.tokenize(text)
        expected_result = [(0, 3, "ریش")]
        self.assertEqual(tokens, expected_result, msg="tokenized single word text must contain a tuple of (0, len(text), word)")

    def test_multi_word_text(self):
        tokenizer = PositionalTokenizer()
        text = "ریش سفیدان"
        tokens = tokenizer.tokenize(text)
        expected_result = [
            (0, 3, "ریش"),
            (4, 10, "سفیدان")
        ]
        self.assertEqual(tokens, expected_result)