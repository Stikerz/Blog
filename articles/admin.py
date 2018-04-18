from django.contrib import admin
from .models import Article

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'status', 'created', 'updated')
    list_filter = ('status',  'created', )
    search_fields = ('title', 'body')

admin.site.register(Article, ArticleAdmin)
