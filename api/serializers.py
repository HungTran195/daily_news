from .models import Article, ArticleContent, Source
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = (
            'source', 'url', 'title', 'thumbnail', 'author', 
            'published_time', 
        )
    
    def get_source(self, article):
        """
        Convert source id to source name
        """
        return article.from_source.name

class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleContent
        fields = (
            'content',
        )
    
