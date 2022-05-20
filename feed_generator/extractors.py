import datetime
import time
import bs4

import feedparser
from requests import request
from django.conf import settings
from api.models import Article, Source

REQUEST_ARTICLE_TIMEOUT = settings.REQUEST_ARTICLE_TIMEOUT
def download_article(url):
    """
    Download data from page and convert to BeautifulSoup object
    """

    response = request.get(url,REQUEST_ARTICLE_TIMEOUT)
    if response.ok:
        return bs4.BeautifulSoup(request.content)
    pass

def get_thumbnail():
    """
    Get thumbnail of the article
    """
    pass


def get_content():
    """
    Extract main content of the article
    """
    pass

def update_news_feed():
    """
    Update database with the latest articles from RSS feed
    """
    all_sources = Source.objects.all()

    for source in all_sources:
        rss_url = source.url
        data = feedparser.parse(rss_url)

        # Extract common information of article
        for entry in data.entries:
            title = entry.title
            url = entry.link
            author = entry.author
            published_time = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed))

            
            # Save article to database if it is not exist
            Article.objects.get_or_create(
                from_source = source,
                topic_id = 1,
                url = url,
                author = author,
                title = title,
                published_time = published_time,
            )


