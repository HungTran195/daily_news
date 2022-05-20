from .models import Article, Source
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'from_source', 'url', 'title', 'thumbnail', 'author', 
            'published_time', 'content', 
        )