from django.core.management.base import BaseCommand
from feed_generator.extractors import update_news_feed

class Command(BaseCommand):
    help = "update database"
    # define logic of command

    def handle(self, *args, **options):
        update_news_feed()
