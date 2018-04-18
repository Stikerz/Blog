from django.test import TestCase
from django.test import Client

from django.contrib.auth import get_user_model

import sys
sys.path.insert(0, ".../accounts")
from accounts .models import Profile
from ..forms import ArticleForm

User = get_user_model()

class ArticleFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        user = User.objects.create(username='BigBob', first_name='Big',
                                   last_name='Bob', )
        Profile.objects.create(user=user, publisher=True)

    # Valid Form Data
    def test_ArticleForm_valid(self):
        form = ArticleForm(data={'title':'Ultra', 'body':'Will super return',
                                 'status': 'Published'})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_ArticleForm_invalid(self):
        form = ArticleForm(data={'title': '', 'body': '',
                                 'status': ''})
        self.assertFalse(form.is_valid())


