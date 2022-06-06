from .models import Article, ArticleContent, Source
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()
    article_link = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = (
            'source', 'url', 'title', 'thumbnail', 'author', 
            'published_time', 'article_link' 
        )
    
    def get_source(self, article):
        """
        Convert source id to source name
        """
        return article.from_source.name

    def get_article_link(self, article):
        """
        Create path to get article content
        """
        request = self.context.get("request")
        article_link = request.build_absolute_uri(f'{article.id}/{article.slug}')
        return article_link

class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleContent
        fields = (
            'content',
        )
    
