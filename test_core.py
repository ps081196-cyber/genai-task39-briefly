import unittest
from types import SimpleNamespace as NS
from core import SAMPLE, validate_text, preview, generate

class CoreTests(unittest.TestCase):
    def test_input_limits(self):
        for text in ['', 'too short', 'word ' * 4000]:
            with self.assertRaises(ValueError):
                validate_text(text)
    def test_preview_preserves_source(self):
        result = preview(SAMPLE)
        self.assertEqual(len(result.splitlines()), 3)
        for line in result.splitlines():
            self.assertIn(line[2:], SAMPLE)
    def test_missing_token(self):
        with self.assertRaises(ValueError):
            generate(SAMPLE, '', 'model', 'Bullet points', 'Short', 'English')
    def test_ai_request_and_response(self):
        captured = {}
        class Client:
            def __init__(self, **kwargs):
                captured.update(kwargs)
            def chat_completion(self, **kwargs):
                captured.update(kwargs)
                return NS(choices=[NS(message=NS(content='A summary.'))])
        self.assertEqual(generate(SAMPLE, 'fake-token', 'test-model', 'Bullet points', 'Short', 'English', Client), 'A summary.')
        self.assertEqual(captured['model'], 'test-model')
        self.assertIn(SAMPLE, captured['messages'][1]['content'])
        self.assertEqual(captured['timeout'], 60)

if __name__ == '__main__':
    unittest.main()
