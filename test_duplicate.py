import unittest
from src.duplicate import similarity, fingerprint

class TestDuplicate(unittest.TestCase):
    def setUp(self):
        self.a = {
            "title": "كيف تتعلم أسرع؟",
            "topic": "التعلم",
            "angle": "التكرار المتباعد",
            "keywords": ["تعلم", "ذاكرة"],
            "content": "التكرار المتباعد يساعد على تثبيت المعلومات في الذاكرة."
        }
        self.b = dict(self.a)
        self.c = {
            "title": "لماذا تنام النباتات؟",
            "topic": "العلوم",
            "angle": "سلوك النباتات",
            "keywords": ["نباتات", "علوم"],
            "content": "بعض النباتات تغير نشاطها ليلًا بطريقة مثيرة للاهتمام."
        }

    def test_identical_is_high(self):
        self.assertGreaterEqual(similarity(self.a, self.b), 0.95)

    def test_different_is_lower(self):
        self.assertLess(similarity(self.a, self.c), 0.78)

    def test_fingerprint_exists(self):
        self.assertEqual(len(fingerprint(self.a)), 64)

if __name__ == "__main__":
    unittest.main()
