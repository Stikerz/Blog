from django.test import TestCase
from django.test import Client

from django.contrib.auth import get_user_model

import sys
sys.path.insert(0, ".../accounts")
from accounts .models import Profile
from ..forms import ArticleForm
from ..models import Article

User = get_user_model()

class ArticleFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        user = User.objects.create(username='BigBob', first_name='Big',
                                   last_name='Bob', )
        user.set_password('smith')
        user.save()
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



    def test_create_articleform_post(self):
        user_login = self.client.login(username="BigBob", password="smith")
        self.assertTrue(user_login)

        obj_count = len(Article.objects.all())
        self.assertEqual(obj_count, 0)

        user = User.objects.get(id=1)

        post_response = self.client.post('/articles/create/',
                                         data={'user': user,
                                               'title': 'JamesBrown',
                                               'status': 'Draft',
                                               'body': 'I know when that hotline bling'})


        self.assertEqual(post_response.status_code, 302)
        self.assertEqual(len(Article.objects.all()), 1)

    def test_update_articleform_post(self):
        user_login = self.client.login(username="BigBob", password="smith")
        self.assertTrue(user_login)
        user = User.objects.get(id=1)

        create_post_response = self.client.post('/articles/create/',
                                                data={'user': user,
                                                      'title': 'JamesBrown',
                                                      'status': 'Draft',
                                                      'body': 'I know when that hotline bling'})

        self.assertEqual(create_post_response.status_code, 302)

        update_post_response = self.client.post('{}/update/'.format(
            create_post_response.url),
            data={'user': user,
                  'title': 'JamesBrown',
                  'status': 'Published',
                  'body': 'I know when that hotline bling'})

        self.assertEqual(update_post_response.status_code, 302)

        article = Article.objects.get(id=1)
        self.assertEqual(article.status, 'Published')
