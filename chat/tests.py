from django.test import TestCase

class SimplePassingTest(TestCase):
    def test_true_is_true(self):
        self.assertTrue(True)
