from django.test import TestCase
from django.contrib.auth import get_user_model

import sys
sys.path.insert(0, ".../accounts")
from accounts .models import Profile
from ..models import Article

User = get_user_model()

class ArticlesViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username='john', first_name='Big',
                                   last_name='Bob')
        user1.set_password('smith')
        user1.save()
        Profile.objects.create(user=user1, publisher=True)

        user2 = User.objects.create(username='BigBob', first_name='Big',
                                   last_name='Bob', )
        user2.set_password('brown')
        user2.save()
        Profile.objects.create(user=user2, publisher=False)

        Article.objects.create(user=user1, title='JamesBrown',
                               status='Draft', body='I know when that '
                                                    'hotline bling')


    def test_articlelist_view_with_user_loggedin(self):
        user_login = self.client.login(username="john", password="smith")
        self.assertTrue(user_login)
        response = self.client.get("/articles/article_list/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/article_list.html")

    def test_articlelist_view_with_user_loggedout(self):
        user_login = self.client.login(username="john", password="smith")
        self.assertTrue(user_login)
        self.client.logout()
        response = self.client.get("/articles/article_list/")
        self.assertEqual(response.status_code, 404)

    def test_article_create_view_user_loggedout(self):
        user_login = self.client.login(username="john", password="smith")
        self.assertTrue(user_login)
        self.client.logout()
        response = self.client.get('/articles/create/')
        self.assertEqual(response.status_code, 404)

    def test_article_create_view_with_publishing_user_loggedin(self):
        user_login = self.client.login(username="john", password="smith")
        self.assertTrue(user_login)
        response = self.client.get('/articles/create/')
        self.assertEqual(response.status_code, 200)

    def test_article_create_view_with_non_publishing_user_loggedin(self):
        user_login = self.client.login(username="BigBob", password="brown")
        self.assertTrue(user_login)
        response = self.client.get('/articles/create/')
        self.assertEqual(response.status_code, 404)

    def test_article_update_view_user_loggedout(self):
        user_login = self.client.login(username="john", password="smith")
        self.assertTrue(user_login)
        self.client.logout()
        article = Article.objects.get(id=1)

        response = self.client.get('/articles/article_list/{}/update/'.format(
            article.slug))
        self.assertEqual(response.status_code, 404)

    def test_article_update_view_with_edit_permissions_user_loggedin(self):
        user_login = self.client.login(username="john", password="smith")
        self.assertTrue(user_login)
        article = Article.objects.get(id=1)

        response = self.client.get('/articles/article_list/{}/update/'.format(
            article.slug))
        self.assertEqual(response.status_code, 200)

    def test_article_update_view_with_non_edit_permissions_user_loggedin(self):
        user_login = self.client.login(username="BigBob", password="brown")
        self.assertTrue(user_login)
        article = Article.objects.get(id=1)

        response = self.client.get('/articles/article_list/{}/update/'.format(
            article.slug))
        self.assertEqual(response.status_code, 404)


    def test_article_detail_view_user_loggedout(self):
        user_login = self.client.login(username="BigBob", password="brown")
        self.assertTrue(user_login)
        self.client.logout()
        article = Article.objects.get(id=1)

        response = self.client.get('/articles/article_list/{}/'.format(
            article.slug))
        self.assertEqual(response.status_code, 404)

    def test_article_detail_view_user_loggedin(self):
        user_login = self.client.login(username="BigBob", password="brown")
        self.assertTrue(user_login)
        article = Article.objects.get(id=1)

        response = self.client.get('/articles/article_list/{}/'.format(
            article.slug))
        self.assertEqual(response.status_code, 200)


    def test_article_delete_view_user_loggedout(self):
        user_login = self.client.login(username="john", password="smith")
        self.assertTrue(user_login)
        self.client.logout()
        article = Article.objects.get(id=1)

        response = self.client.get('/articles/article_list/{}/delete/'.format(
            article.slug))
        self.assertEqual(response.status_code, 404)

    def test_article_delete_view_with_edit_permissions_user_loggedin(self):
        user_login = self.client.login(username="john", password="smith")
        self.assertTrue(user_login)

        self.assertEqual(len(Article.objects.all()), 1)
        article = Article.objects.get(id=1)

        response = self.client.get('/articles/article_list/{}/delete/'.format(
            article.slug))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Article.objects.all()), 0)

    def test_article_delete_view_with_non_edit_permissions_user_loggedin(self):
        user_login = self.client.login(username="BigBob", password="brown")
        self.assertTrue(user_login)
        article = Article.objects.get(id=1)

        response = self.client.get('/articles/article_list/{}/delete/'.format(
            article.slug))
        self.assertEqual(response.status_code, 404)

    def test_article_like_view_user_loggedin(self):
        user_login = self.client.login(username="john", password="smith")
        self.assertTrue(user_login)
        article = Article.objects.get(id=1)
        self.assertEqual(len(article.likes.all()), 0)

        response = self.client.get('/articles/article_list/{}/like/'.format(
            article.slug))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(article.likes.all()), 1)

    def test_article_like_view_user_loggedout(self):
        user_login = self.client.login(username="BigBob", password="brown")
        self.assertTrue(user_login)
        self.client.logout()
        article = Article.objects.get(id=1)

        response = self.client.get('/articles/article_list/{}/like/'.format(
            article.slug))
        self.assertEqual(response.status_code, 404)




