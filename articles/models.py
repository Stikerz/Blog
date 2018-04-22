from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse


# Create your models here.

class Article(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    STATUS_CHOICES= (('Published', 'Published'), ('Draft', 'Draft'))
    title = models.CharField(max_length=250)
    body = models.TextField()
    status = models.CharField(max_length=10, default='Draft', choices=STATUS_CHOICES)
    likes = models.ManyToManyField(User, blank=True,
                                   related_name='article_likes')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def get_likes_url(self):
        return reverse("articles:like", kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse("articles:article_update", kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse("articles:article_delete", kwargs={'slug': self.slug})


    def __str__(self):
        return self.title

