from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

class AccountViewsTest(TestCase):

    def setUp(self):
        self.user  = User.objects.create(username='john', first_name='Big',
                                   last_name='Bob')
        self.user.set_password('smith')
        self.user.save()

    def test_login_view_with_user_loggedin(self):
        user_login = self.client.login(username="john", password="smith")
        self.assertTrue(user_login)
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 302)

    def test_login_view_with_user_loggedout(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_register_view_user_loggedout(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_register_view_with_user_loggedin(self):
        user_login = self.client.login(username="john", password="smith")
        self.assertTrue(user_login)
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        user_login = self.client.login(username="john", password="smith")
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)






