from django.apps import AppConfig
import nltk


class RaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ra_app'

    def ready(self):
        # NLTK 'punkt' tokenizer downloaded and available
        nltk.download('punkt')
