# Generated by Django 5.0.2 on 2024-03-06 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ra_app', '0003_favouritepaper_delete_searchhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='favouritepaper',
            name='publication_info',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='favouritepaper',
            name='snippet',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
