from django.test import TestCase
from django.test import Client
from django import forms
from django.contrib.auth import get_user_model

import sys
sys.path.insert(0, ".../accounts")
from accounts .models import Profile
from ..forms import RegisterForm, LoginForm, ProfileForm

User = get_user_model()

class ArticleFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        user = User.objects.create(username='BigBob', first_name='Big',
                                   last_name='Bob', password='itsasecret')
        Profile.objects.create(user=user, publisher=True)

    # Invalid Form Data
    def test_ArticleForm_invalid(self):
        data = {'username':'' , 'password':''}
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())


    # Valid Form Data
    def test_LoginForm_valid(self):
        user = User.objects.get(id=1)
        data = {'username': user.username, 'password': user.password}
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_Register_Form_valid(self):
        user = User.objects.get(id=1)
        data = {'username': 'mrpresident', 'password': 'trump'}
        form = RegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_Register_Form_invalid(self):
        user = User.objects.get(id=1)
        data = {'username': '', 'password': ''}
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())


    def test_ProfileForm_valid(self):
        user = User.objects.get(id=1)
        data = {'publisher': True}
        form = ProfileForm(data=data)
        self.assertTrue(form.is_valid())






