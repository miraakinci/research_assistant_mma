from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ra_app.models import Article, FavouritePaper
from django.contrib.messages import get_messages
import json

User = get_user_model()


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.article = Article.objects.create(title='Test Article', authors='Author Name',
                                              link='http://example.com/article')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_signup_view_post_valid(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'newPassword': 'password123',
            'newPassword2': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('login'), {
            'username': self.user.username,
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 302)  # Redirect even if invalid
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Invalid username or password.')

    def test_feed_view_not_logged_in_redirects(self):
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 302)  # Should redirect if not logged in
        self.assertRedirects(response, '/login/?next=/feed/')  # Default login url

    def test_feed_view_logged_in(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')

    # Add more tests for other views like search_results_view, save_paper_view, etc.


class SearchAndViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.article = Article.objects.create(title='Test Article', authors='Author Name', link='http://example.com/article')

    def test_search_results_view_post_valid(self):
        # User must be logged in to search
        self.client.login(username='testuser', password='password123')

        with self.settings(DEBUG=True):  # Ensure we can use the Django test client for AJAX calls
            response = self.client.post(reverse('search_results'), {
                'query': 'test'
            }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')

        # Assuming your view is returning the context with articles_data
        self.assertTrue('articles_data' in response.context)

    def test_save_paper_view(self):
        self.client.login(username='testuser', password='password123')
        paper_data = {
            'title': 'New Article',
            'link': 'http://newarticle.com',
            'authors': 'New Author',
            'publication_info': 'New Publication Info',
            'abstract': 'New Abstract',
        }

        response = self.client.post(reverse('save_paper'), json.dumps(paper_data),
                                    content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Article.objects.filter(title='New Article').exists())
        self.assertTrue(FavouritePaper.objects.filter(user=self.user, article__title='New Article').exists())

        response_content = json.loads(response.content)
        self.assertEqual(response_content['message'], 'Article saved to favourites')

    def test_unsave_paper_view(self):
        self.client.login(username='testuser', password='password123')
        favourite_paper = FavouritePaper.objects.create(user=self.user, article=self.article)

        response = self.client.post(reverse('unsave_paper', kwargs={'paper_id': self.article.id}),
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(FavouritePaper.objects.filter(pk=favourite_paper.pk).exists())

        response_content = json.loads(response.content)
        self.assertEqual(response_content['message'], 'Paper unsaved successfully')
