from models import Article, ArticleContent


all_articles = Article.objects.all()

for article in all_articles:
    content = article.content
    article_id = article.id

    ArticleContent.create(
        article_id = article_id,
        content = content
    )
