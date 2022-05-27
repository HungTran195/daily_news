from django.contrib import admin
from .models import Topic, Source, Article, ArticleContent

admin.site.register(Topic)
admin.site.register(Source)
admin.site.register(Article)
admin.site.register(ArticleContent)

