from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# Create your models here.

class Article(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    STATUS_CHOICES= (('Published', 'Published'), ('Draft', 'Draft'))
    title = models.CharField(max_length=250)
    body = models.TextField()
    status = models.CharField(max_length=10, default='Draft', choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

