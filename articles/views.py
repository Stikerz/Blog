from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Article
from .forms import ArticleForm

from accounts .models import Profile

from comments .models import Comment
from comments .forms import CommentForm


# Create your views here.

def article_create(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if profile.is_publisher:
            template = 'articles/article_form.html'
            form = ArticleForm(request.POST or None)
            if form.is_valid():
                title = form.cleaned_data.get("title")
                status = form.cleaned_data.get("status")
                body = form.cleaned_data.get("body")
                article= Article.objects.create(user=request.user,
                                                 title=title, body=body,
                                                 status=status)
                return HttpResponseRedirect('/articles/article_list/{}'.format(
                    article.slug))
            context = {'form':form}
            return render(request, template, context)
        else:
            raise Http404("Page cannot be found")
    else:
        raise Http404("Page cannot be found")


def article_update(request, slug):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        article = get_object_or_404(Article, slug=slug)
        if profile.is_publisher and article.user==request.user:
            template = 'articles/article_form.html'

            form = ArticleForm(request.POST or None, instance= article)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/articles/article_list/{}'.format(
                    instance.slug))
            context = {'title': article.title, 'article': article, 'form': form}
            return render(request, template, context)
        else:
            raise Http404("Page cannot be found")

    else:
        raise Http404("Page cannot be found")

def article_delete(request, slug):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        article = get_object_or_404(Article, slug=slug)
        if profile.is_publisher and article.user == request.user:
            article = get_object_or_404(Article, slug = slug)
            article.delete()
            return redirect("articles:article_list_view")
        else:
            raise Http404("Page cannot be found")
    else:
        raise Http404("Page cannot be found")

def article_list(request):
    if request.user.is_authenticated:
        template = 'articles/article_list.html'
        query_set = Article.objects.all().order_by('-updated')
        query = request.GET.get("query")
        if query:
            query_set = query_set.filter(title__icontains=query)
        paginator = Paginator(query_set, 5)
        page = request.GET.get('page')
        object_list = paginator.get_page(page)
        context = {'object_list': object_list, 'request': request}

        return render(request, template, context)
    else:
        raise Http404("Page cannot be found")





def article_detail(request, slug):
    if request.user.is_authenticated:
        template = 'articles/article_detail.html'
        article = get_object_or_404(Article, slug = slug)
        content_type = ContentType.objects.get_for_model(Article)
        obj_id = article.id
        initial_data = {'content_type': content_type,
                        'object_id': obj_id}
        comments = Comment.objects.filter(content_type=content_type,
                                          object_id=obj_id)

        comments_form = CommentForm(request.POST or None, instance=article,
                                    initial=initial_data)

        if comments_form.is_valid():
            content_data = comments_form.cleaned_data.get("content")
            new_comment, created = Comment.objects.get_or_create(user=
                                                                 request.user,
                                                                 content_type=
                                                                 content_type,
                                                                 object_id =obj_id,
                                                                 content=content_data)
        context = {'article': article, 'comments': comments,
                   'comments_form': comments_form}

        return render(request, template, context)
    else:
        raise Http404("Page cannot be found")

def article_likes_toggle(request, slug):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, slug=slug)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)
        return HttpResponseRedirect('/articles/article_list/{}'.format(
                    article.slug))

    else:
        raise Http404("Page cannot be found")


