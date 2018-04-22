from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Article
from django.template.defaultfilters import slugify
User = get_user_model()

class ArticleModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        user = User.objects.create(username='BigBob', first_name='Big',
                                   last_name='Bob')
        Article.objects.create(user=user, title = 'JamesBrown',
                               status='Draft', body='I know when that '
                                                    'hotline bling')


    def test_title_label(self):
        article=Article.objects.get(id=1)
        field_label = article.title
        self.assertEquals(field_label, 'JamesBrown')

    def test_body_label(self):
        article=Article.objects.get(id=1)
        field_label = article.body
        self.assertEquals(field_label, 'I know when that hotline bling')

    def test_status_label(self):
        article=Article.objects.get(id=1)
        field_label = article.status
        self.assertEquals(field_label, 'Draft')

    def test_title_max_length(self):
        article=Article.objects.get(id=1)
        max_length = article._meta.get_field('title').max_length
        self.assertEquals(max_length, 250)

    def test_object_name_is_title(self):
        article=Article.objects.get(id=1)
        title = article.title
        self.assertEquals(title, str(article))

    def test_get_delete_url(self):
        article = Article.objects.get(id=1)
        slug_title = slugify(article.title)
        article_delete_url = article.get_delete_url()

        self.assertEquals(article_delete_url, "/articles/article_list/{"
                                              "}/delete/".format(slug_title))

    def test_get_update_url(self):
        article = Article.objects.get(id=1)
        slug_title = slugify(article.title)
        article_update_url = article.get_update_url()

        self.assertEquals(article_update_url, "/articles/article_list/{"
                                              "}/update/".format(slug_title))

    def test_get_like_url(self):
        article = Article.objects.get(id=1)
        slug_title = slugify(article.title)
        article_like_url = article.get_likes_url()

        self.assertEquals(article_like_url, "/articles/article_list/{"
                                              "}/like/".format(slug_title))



