from .models import Article
from django.views.generic import ListView


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
