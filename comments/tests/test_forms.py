from django.test import TestCase
from django.contrib.auth import get_user_model

from ..forms import CommentForm
from ..models import Comment

import sys
sys.path.insert(0, ".../accounts")
from accounts .models import Profile

sys.path.insert(0, ".../articles")
from articles .models import Article

User = get_user_model()

class CommentFormTest(TestCase):

    # Valid Form Data
    def test_CommentForm_valid(self):
        form = CommentForm(data={'content':'just another day'})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_CommentForm_invalid(self):
        form = CommentForm(data={'content': ''})
        self.assertFalse(form.is_valid())

    def test_create_comment_form_post(self):
        user = User.objects.create(username='BigBob', first_name='Big',
                                   last_name='Bob', )
        user.set_password('smith')
        user.save()
        Profile.objects.create(user=user, publisher=True)

        user_login = self.client.login(username="BigBob", password="smith")
        self.assertTrue(user_login)

        obj_count = len(Article.objects.all())
        self.assertEqual(obj_count, 0)

        user = User.objects.get(id=1)

        create_article_post_response = self.client.post('/articles/create/',
                                         data={'user': user,
                                               'title': 'JamesBrown',
                                               'status': 'Draft',
                                               'body': 'I know when that hotline bling'})


        self.assertEqual(create_article_post_response.status_code, 302)
        self.assertEqual(len(Article.objects.all()), 1)

        self.assertEqual(len(Comment.objects.all()), 0)

        create_comment_post_response = self.client.post('{}/'.format(
            create_article_post_response.url),
            data={'content': 'I know when that hotline bling'})

        self.assertEqual(create_comment_post_response.status_code, 200)
        self.assertEqual(len(Comment.objects.all()), 1)



