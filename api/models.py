from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify 


class Topic(models.Model):
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=125)
    url = models.URLField()


    def __str__(self):
        return self.name

class Article(models.Model):
    from_source = models.ForeignKey(Source,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.SET_DEFAULT, default='General')
    url = models.URLField(unique=True, max_length=255)
    title = models.CharField(max_length=255)
    thumbnail = models.URLField(blank=True, max_length=255)
    author = models.CharField(max_length=250, blank=True)
    published_time = models.DateTimeField()
    slug = models.SlugField(null=False, max_length=255)
    is_scraping = models.BooleanField(default=True)

    created_at= models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ("published_time",)

    def __str__(self):
        return f'{self.from_source} | {self.title}'

    def get_absolute_url(self):
        return reverse('news_feed:article_detail', kwargs={'slug': self.slug, 'pk': self.id})

    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class ArticleContent(models.Model):
    article_id = models.OneToOneField(Article, on_delete=models.CASCADE)
    content = models.TextField(blank=True)

    def __str__(self):
        return f'{self.article_id}'