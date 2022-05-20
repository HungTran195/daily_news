from django.test import TestCase
from api.models import Topic, Source, Article
from django.utils import timezone
import datetime

class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Run once to set up non-modified data for all class methods
        pass

    def setUp(self):
        # Run once for every test method to setup clean data
        time = timezone.now() + datetime.timedelta(days=30)
        Topic.objects.create(name = 'new_topic')
        Source.objects.create(name='Theverge', url ='http://theverge.com')

        Article.objects.create(
            from_source_id = 1, 
            topic_id = 1, 
            url = 'https://www.theverge.com/23123317/sony-linkbuds-s-earbuds-headphones-review',
            title = 'SONY LINKBUDS S REVIEW: SUPREME COMFORT DOESN''T COME CHEAP', 
            thumbnail = 'https://cdn.vox-cdn.com/thumbor/1DAKCpIjbrXBu7E-Dsd8hTVbf3A=/0x0:2040x1360/3820x2149/filters:focal(948x778:1274x1104):format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/70883393/DSCF7987.0.jpg', 
            author = 'Chris Welch', 
            published_time = time, 
            content = '', 
            slug = 'sony-linkbuds-s-earbuds-headphones-review', 
            is_scraping = False
        )


    def test_model_topic_str_method(self):
        topic = Topic.objects.get(name = 'new_topic')
        self.assertEqual(str(topic), 'new_topic')

    def test_model_source_str_method(self):
        source = Source.objects.get(name = 'Theverge')
        self.assertEqual(str(source), 'Theverge')

    def test_model_article_str_method(self):
        article = Article.objects.get(id = 1)
        self.assertEqual(str(article), 'Theverge | SONY LINKBUDS S REVIEW: SUPREME COMFORT DOESN''T COME CHEAP')
    
    def test_article_get_absolute_url(self):
        #TODO create test for this function
        pass