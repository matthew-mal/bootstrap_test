from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, FormView, CreateView, DetailView, DeleteView, UpdateView

from .models import Article
from .forms import CommentForm


class CommentPost(SingleObjectMixin, FormView):
    """
    View class for posting comments on an article.
    Requires user authentication.
    """
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("article_list")


class ArticleListView(LoginRequiredMixin, ListView):
    """
    View class for displaying a list of articles.
    Requires user authentication.
    """
    model = Article
    template_name = 'article_list.html'


class ArticleDetailView(LoginRequiredMixin, DetailView):
    """
    View class for displaying details of a single article, including comments form.
    Requires user authentication.
    """
    model = Article
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View class for deleting an article.
    Requires user authentication and author permission.
    """
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View class for updating an article.
    Requires user authentication and author permission.
    """
    model = Article
    fields = (
        'title',
        'body'
    )
    template_name = 'article_edit.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    View class for creating a new article.
    Requires user authentication.
    """
    model = Article
    template_name = 'article_new.html'
    fields = (
        'title',
        'body',
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentGet(DeleteView):
    """
    View class for handling GET request for comments on an article.
    """
    model = Article
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
