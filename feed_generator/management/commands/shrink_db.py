from django.core.management.base import BaseCommand
from api.models import Article
import datetime

class Command(BaseCommand):
    help = "update database"


    def handle(self, *args, **options):
        # Remove articles that is more than 1 month old 
        # to keep the database small enough in free tire!
        year, week, _ = datetime.date.today().isocalendar()
        query = Article.objects.filter(published_time__year=year).filter(published_time__week__lt=week-4)
        query.delete()
