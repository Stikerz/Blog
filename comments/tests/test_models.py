from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

import sys
sys.path.insert(0, ".../articles")
from ..models import Comment
from articles .models import Article
User = get_user_model()

class CoomentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        user = User.objects.create(username='BigBob', first_name='Big',
                                   last_name='Bob')
        article = Article.objects.create(user=user, title = 'JamesBrown',
                               status='Draft', body='I know when that '
                                                    'hotline bling')
        content_type = ContentType.objects.get_for_model(Article)

        comment = "just another comment"

        Comment.objects.create(user=user,content_type=content_type,
                               object_id =article.id, content=comment)


    def test_object_content_type(self):
        comment = Comment.objects.get(id=1)
        content_type = ContentType.objects.get_for_model(Article)
        self.assertEqual(comment.content_type, content_type)

    def test_comment_content(self):
        comment = Comment.objects.get(id=1).content
        self.assertEqual(comment, 'just another comment')

    def test_object_name_is_username(self):
        comment = Comment.objects.get(id=1)
        username = comment.user.username
        self.assertEquals(username, str(comment))



