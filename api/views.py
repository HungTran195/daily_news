from django.core import exceptions
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ArticleDetailSerializer, ArticleSerializer

from .models import Article, ArticleContent


class ArticleView(generics.ListAPIView):
    """
    Retrieve details of articles from the database
    """

    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        queryset = Article.objects.all()
        keyword = self.request.query_params.get('q')
        if keyword is not None:
            queryset = queryset.filter(title__icontains = keyword)
        return queryset

class ArticleDetailsView(APIView):
    """
    Retrieve detail of the article
    """
    authentication_classes = [] 
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        slug = kwargs.get('slug')
        try:
            content = ArticleContent.objects.get(article_id = pk)
        except exceptions.ObjectDoesNotExist:
            return Response(data = [], status = status.HTTP_404_NOT_FOUND)

        serializer = ArticleDetailSerializer(content)
        return Response(data = serializer.data, status = status.HTTP_200_OK)


class TopicView(generics.ListAPIView):
    """
    Retrieve all articles with the same topic
    """
    pass
