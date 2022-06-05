from re import L
from django.test import TestCase
from api.models import ArticleContent, Topic, Source, Article
from api.serializers import ArticleSerializer
from django.utils import timezone
import datetime
from django.urls import reverse
class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Run once to set up non-modified data for all class methods
        time = datetime.datetime.now()
        topic = Topic.objects.create(name = 'new_topic')
        source = Source.objects.create(name='Theverge', url ='http://theverge.com')

        article = Article.objects.create(
            from_source = source, 
            topic = topic, 
            url = 'https://www.dummy.com/',
            title = 'SONY LINKBUDS S REVIEW: SUPREME COMFORT DOESN''T COME CHEAP', 
            thumbnail = 'https://cdn.vox-cdn.com/thumbor/', 
            author = 'Chris Welch', 
            published_time = time, 
            slug = 'sony-linkbuds-s-earbuds-headphones-review', 
            is_scraping = False
        )


    def setUp(self):
        # Run once for every test method to setup clean data
        pass


    def test_model_topic_str_method(self):
        topic = Topic.objects.get(name = 'new_topic')
        self.assertEqual(str(topic), 'new_topic')

    def test_model_source_str_method(self):
        source = Source.objects.get(name = 'Theverge')
        self.assertEqual(str(source), 'Theverge')
    
    def test_model_article_str_method(self):
        article = Article.objects.get(url = 'https://www.dummy.com/')
        self.assertEqual(str(article), 'Theverge | SONY LINKBUDS S REVIEW: SUPREME COMFORT DOESN''T COME CHEAP')
    
    def test_article_get_absolute_url(self):
        article = Article.objects.get(url ='https://www.dummy.com/')
        self.assertEqual('/api/articles/1/sony-linkbuds-s-earbuds-headphones-review', article.get_absolute_url())
    
    def test_article_slugify(self):
        article = Article.objects.create(
            from_source_id = 1, 
            topic_id = 1, 
            url = 'https://www.dummy.com/1',
            title = 'Dummy title',
            author = 'Chris Welch', 
            published_time = datetime.datetime.now(), 
            is_scraping = False
        )

        self.assertEqual('dummy-title', article.slug)

    def test_article_content(self):
        article = Article.objects.get(url ='https://www.dummy.com/')
        article_content = ArticleContent.objects.create(
            article_id_id = 1,
            content = 'Dummy content'
        )
        self.assertEqual(str(article), str(article_content))

    def test_article_serializer(self):
        article = Article.objects.get(url ='https://www.dummy.com/')
        serializer = ArticleSerializer(article)
        data = serializer.data
        self.assertEqual('Theverge',data['source'])
        self.assertEqual('1/sony-linkbuds-s-earbuds-headphones-review', data['article_link'])
