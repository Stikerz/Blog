from django.urls import path

from .views import article_detail, article_list, article_create, \
    article_update, article_delete

urlpatterns = [

    path('article_list/', article_list, name='article_list_view'),
    path('article_list/<slug:slug>/', article_detail,
         name='article_detailed_view'),
    path('create/', article_create, name='article_create'),
    path('article_list/<slug:slug>/update/', article_update,
         name='article_update'),
    path('article_list/<slug:slug>/delete/', article_delete, name='article_delete'),
]
