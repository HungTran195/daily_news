# Generated by Django 4.0.4 on 2022-05-26 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_articles_id_articlecontent_article_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='content',
        ),
    ]
