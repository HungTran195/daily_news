from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from api.serializers import ArticleDetailSerializer, ArticleSerializer
from django.core import exceptions
from .models import Article, ArticleContent
from rest_framework.permissions import AllowAny

class ArticleView(generics.ListAPIView):
    """
    Retrieve details of articles from the database
    """

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()



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


class TopicView(DetailView):
    """
    Retrieve all articles with the same topic
    """
    pass
