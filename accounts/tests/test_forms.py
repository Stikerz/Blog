from django.test import TestCase
from django.contrib.auth import get_user_model

import sys
sys.path.insert(0, ".../accounts")
from accounts .models import Profile
from ..forms import RegisterForm, LoginForm, ProfileForm

User = get_user_model()

class AccountsFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        user = User.objects.create(username='john', first_name='Big',
                                   last_name='Bob')
        user.set_password('smith')
        user.save()
        Profile.objects.create(user=user, publisher=True)

    # Invalid Form Data
    def test_ArticleForm_invalid(self):
        data = {'username':'' , 'password':''}
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())


    # Valid Form Data
    def test_LoginForm_valid(self):
        user = User.objects.get(id=1)
        data = {'username': user.username, 'password': 'smith'}
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

    def test_loginform_post_loggedout(self):
        user_login = self.client.login(username="john", password="smith")
        self.assertTrue(user_login)
        self.client.logout()

        get_response = self.client.get("/login/")
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post('/login/', data={'username': 'john',
                                                 'password':
            'smith'})

        self.assertEqual(post_response.status_code, 302)

    def test_registerform_post(self):
        user_login = self.client.login(username="john", password="smith")
        self.assertTrue(user_login)
        get_response_loggedin = self.client.get("/register/")
        self.assertEqual(get_response_loggedin.status_code, 302)
        self.client.logout()

        get_response = self.client.get("/register/")
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post('/register/', data={'username':
                                                                 'james',
                                                 'password':
            'brown'})

        self.assertEqual(post_response.status_code, 302)






