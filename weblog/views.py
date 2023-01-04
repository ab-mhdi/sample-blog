from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Article, Category
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


# from django.http import HttpResponse, JsonResponse


# Create your views here.
# def home(request, page=1):
#     Article_List = Article.objects.published()
#     paginator = Paginator(Article_List, 3)
#     article = paginator.get_page(page)
#     context = {
#         'articles': article,
#     }
#     return render(request, 'weblog/article_list.html', context)
class ArticleList(ListView):
    # model = Article
    # template_name = 'weblog.login.html'
    # context_object_name = "articles"
    queryset = Article.objects.published()
    paginate_by = 3


class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article, slug=slug)


# def detail(request, slug):
#     context = {
#         'article': get_object_or_404(Article, slug=slug)
#     }
#     return render(request, 'weblog/article_detail.html', context)


# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     article_list = category.article.published()
#     paginator = Paginator(article_list, 3)
#     articles = paginator.get_page(page)
#     context = {
#         'category': category,
#         'articles': articles,
#     }
#     return render(request, 'weblog/category_list.html', context)
class CategoryList(ListView):
    paginate_by = 3
    template_name = 'weblog/category_list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.article.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context

class AuthorList(ListView):
    paginate_by = 3
    template_name = 'weblog/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.article.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context