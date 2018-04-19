from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Profile

User = get_user_model()

class AccountModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        user = User.objects.create(username='BigBob', first_name='Big',
                                   last_name='Bob')
        Profile.objects.create(user=user, publisher=True)

    def test_getter_is_publisher(self):
        profile=Profile.objects.get(id=1)
        is_publisher = profile.is_publisher
        self.assertEquals(is_publisher, True)

    def test_object_name_is_formatted_username(self):
        profile=Profile.objects.get(id=1)
        username = profile.user.username
        obj_name = "{}'s Profile".format(username)
        self.assertEquals(obj_name, str(profile))

    def test_setter_set_user_and_publisher(self):
        user = User.objects.create(username='Godsplan', first_name='Drake',
                                   last_name='Canada')
        profile = Profile()
        profile.set_publisher(True)
        profile.set_user(user)
        profile.save()
        new_profile = Profile.objects.get(id=2)
        is_publisher = profile.is_publisher

        self.assertEqual(user,new_profile.user)
        self.assertEquals(is_publisher, True)


