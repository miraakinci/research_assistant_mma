from django.test import TestCase
from django.core.exceptions import ValidationError
from ra_app.models import User, Article, FavouritePaper

class UserModelTest(TestCase):

    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            bio='A short bio here.'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.bio, 'A short bio here.')
        self.assertTrue(user.is_active)

    def test_user_username_validator(self):
        with self.assertRaises(ValidationError):
            user = User(username='usr', email='test@example.com')
            user.full_clean()

    def test_user_email_validator(self):
        with self.assertRaises(ValidationError):
            user = User(username='testuser', email='invalid-email')
            user.full_clean()

class ArticleModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            bio='A short bio here.'
        )

    def test_article_creation(self):
        article = Article.objects.create(
            title='Test Article',
            authors='Author Name',
            link='http://example.com/article',
            publication_info='Test Journal, 2024',
            abstract='This is a test abstract.'
        )
        self.assertEqual(article.title, 'Test Article')
        self.assertEqual(article.authors, 'Author Name')
        self.assertEqual(article.link, 'http://example.com/article')
        self.assertEqual(article.publication_info, 'Test Journal, 2024')
        self.assertEqual(article.abstract, 'This is a test abstract.')

    def test_article_string_representation(self):
        article = Article.objects.create(
            title='Test Article',
            authors='Author Name'
        )
        self.assertEqual(str(article), 'Test Article')

    def test_article_favourited_by_many_users(self):
        article = Article.objects.create(
            title='Test Article',
            authors='Author Name',
            link='http://example.com/article'
        )
        article.favourited_by.add(self.user)
        self.assertIn(self.user, article.favourited_by.all())

class FavouritePaperModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.article = Article.objects.create(
            title='Test Article',
            authors='Author Name',
            link='http://example.com/article'
        )

    def test_favourite_paper_creation(self):
        favourite = FavouritePaper.objects.create(
            user=self.user,
            article=self.article
        )
        self.assertEqual(favourite.user.username, 'testuser')
        self.assertEqual(favourite.article.title, 'Test Article')

    def test_favourite_paper_string_representation(self):
        favourite = FavouritePaper.objects.create(
            user=self.user,
            article=self.article
        )
        self.assertEqual(str(favourite), 'Test Article')

    def test_favourite_paper_without_article(self):
        favourite = FavouritePaper.objects.create(
            user=self.user
        )
        self.assertIsNone(favourite.article)
        self.assertEqual(str(favourite), 'Unknown Article')

    def test_favourite_paper_cascade_delete(self):
        favourite = FavouritePaper.objects.create(
            user=self.user,
            article=self.article
        )
        # Deleting the article should also delete the associated favourite paper
        self.article.delete()
        with self.assertRaises(FavouritePaper.DoesNotExist):
            FavouritePaper.objects.get(pk=favourite.pk)

        # Creating another favourite for testing cascade delete on user
        new_article = Article.objects.create(
            title='Another Article',
            authors='Another Author',
            link='http://example.com/another-article'
        )
        new_favourite = FavouritePaper.objects.create(
            user=self.user,
            article=new_article
        )
        # Deleting the user should also delete the associated favourite paper
        self.user.delete()
        with self.assertRaises(FavouritePaper.DoesNotExist):
            FavouritePaper.objects.get(pk=new_favourite.pk)

