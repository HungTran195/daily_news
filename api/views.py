from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from rest_framework import generics

from api.serializers import ArticleSerializer

from .models import Article


class ArticleView(generics.ListAPIView):
    """
    Retrieve all articles from database
    """

    serializer_class = ArticleSerializer
    queryset = Article.objects.all().order_by('-id')



class ArticleDetailsView(DetailView):
    """
    Retrieve detail of the article
    """
    def get(self,request, *args, **kwargs):
        return HttpResponse('Detail view')
    pass

class TopicView(DetailView):
    """
    Retrieve all articles with the same topic
    """
    pass
