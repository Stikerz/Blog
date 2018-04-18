from django.test import TestCase
from django.test import Client

from django.contrib.auth import get_user_model

from ..forms import CommentForm

User = get_user_model()

class ArticleFormTest(TestCase):

    # Valid Form Data
    def test_ArticleForm_valid(self):
        form = CommentForm(data={'content':'just another day'})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_ArticleForm_invalid(self):
        form = CommentForm(data={'content': ''})
        self.assertFalse(form.is_valid())
