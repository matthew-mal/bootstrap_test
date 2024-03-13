from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Article, Comment
from .forms import CommentForm

CustomUser = get_user_model()


class ArticleViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.article = Article.objects.create(title='Test Article', body='This is a test article.', author=self.user)

    def test_article_list_view(self):
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_list.html')

    def test_article_detail_view(self):
        response = self.client.get(reverse('article_detail', kwargs={'pk': self.article.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_detail.html')

    def test_article_create_view(self):
        response = self.client.post(reverse('article_new'),
                                    {'title': 'New Test Article', 'body': 'This is a new test article.'})
        self.assertEqual(response.status_code, 302)  # Redirects to article list upon successful creation
        self.assertTrue(Article.objects.filter(title='New Test Article').exists())

    def test_article_update_view(self):
        response = self.client.post(reverse('article_edit', kwargs={'pk': self.article.pk}),
                                    {'title': 'Updated Test Article', 'body': 'This is an updated test article.'})
        self.assertEqual(response.status_code, 302)  # Redirects to article list upon successful update
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Test Article')

    def test_article_delete_view(self):
        response = self.client.post(reverse('article_delete', kwargs={'pk': self.article.pk}))
        self.assertEqual(response.status_code, 302)  # Redirects to article list upon successful deletion
        self.assertFalse(Article.objects.filter(title='Test Article').exists())

    def test_comment_form(self):
        form_data = {'comment': 'Test comment text', 'author': self.user.pk}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_comment_get_view(self):
        response = self.client.get(reverse('article_detail', kwargs={'pk': self.article.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_detail.html')
        self.assertIsInstance(response.context['form'], CommentForm)
