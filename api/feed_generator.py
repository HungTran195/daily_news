import datetime
import time

import feedparser

from .models import Article, Source


def update_news_feed():
    """
    Update database with the latest articles from RSS feed
    """
    all_sources = Source.objects.all()

    for source in all_sources:
        rss_url = source.url
        data = feedparser.parse(rss_url)

        # Extract common article information from data entry
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


