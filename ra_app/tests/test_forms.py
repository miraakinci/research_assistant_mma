from django.test import TestCase
from ra_app.forms import LogInForm, SignUpForm, FavouritePaperForm, SearchForm
from ra_app.models import User, Article, FavouritePaper

class LogInFormTest(TestCase):
    def test_valid_data(self):
        form = LogInForm(data={
            'username': 'john',
            'password': '12345'
        })
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = LogInForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)

class SignUpFormTest(TestCase):
    def test_valid_data(self):
        # Ensuring that data is valid including matching passwords
        form_data = {
            'username': 'johnny',  # Username meets minimum requirements
            'email': 'john@example.com',
            'newPassword': '12345678',
            'passwordConfirmation': '12345678'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_password_mismatch(self):
        # Ensuring the form is invalid when passwords do not match
        form_data = {
            'username': 'johnny',
            'email': 'john@example.com',
            'newPassword': '12345678',
            'passwordConfirmation': '87654321'  # Different password
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('passwordConfirmation', form.errors)
        self.assertEqual(form.errors['passwordConfirmation'], ['Password confirmation does not match Password'])

    def test_invalid_email(self):
        # Testing the email validation
        form_data = {
            'username': 'johnny',
            'email': 'notanemail',  # Invalid email
            'newPassword': '12345678',
            'passwordConfirmation': '12345678'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_required_fields(self):
        # Ensure that all fields are required
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('newPassword', form.errors)
        self.assertIn('passwordConfirmation', form.errors)

class FavouritePaperFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='john', email='john@example.com')
        self.article = Article.objects.create(title='Test Article', authors='Author Name', link='http://example.com')

    def test_valid_data(self):
        form = FavouritePaperForm(data={'article': self.article.id}, user=self.user)
        self.assertTrue(form.is_valid())

    def test_save_form(self):
        form = FavouritePaperForm(data={'article': self.article.id}, user=self.user)
        if form.is_valid():
            instance = form.save()
            self.assertEqual(instance.user, self.user)
            self.assertEqual(instance.article, self.article)

class SearchFormTest(TestCase):
    def test_valid_data(self):
        form = SearchForm(data={'query': 'Test Query'})
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = SearchForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('query', form.errors)
