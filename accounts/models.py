from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,
                             on_delete=models.CASCADE)
    publisher = models.BooleanField(default=False)

    def set_user(self, user):
        self.user = user

    def set_publisher(self, publisher):
        self.publisher = publisher

    @property
    def is_publisher(self):
        return self.publisher

    def __str__(self):
        return "{}'s Profile".format(self.user.username)
