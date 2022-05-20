from django.urls import path
from .views import ArticleView, ArticleDetailsView, TopicView

app_name = 'news_feed'

urlpatterns = [
    path('', ArticleView.as_view(), name='article_list'),
    path('articles/<int:pk>/<slug:slug>', ArticleDetailsView.as_view(), name='article_detail'),
    path('topic/<str:topic>/<slug:slug>', TopicView.as_view(), name='topic_detail'),
    # path('/about', ),
]
