# daily_news


Daily news is a REST API used to generate custom news feed to keep you up to date with the latest articles from your favorite news website.

Check out the API link: [https://my-daily-news.herokuapp.com/api/articles](https://my-daily-news.herokuapp.com/api/articles)

#### Endpoints:

The anatomy of an endpoint should look like this:

- `/api/articles` and `/api/articles?page={page_number}` : Retrieve latest articles
- `/api/articles/{article_id}/{slug}` :  used to get content extracted from the original article.

*Example of a response:*

- From `api/articles` or  `/api/articles?page={page_number}:`

```other
{
	"count": 772,
	"next": "https://my-daily-news.herokuapp.com/api/articles?page=3",
	"previous": "https://my-daily-news.herokuapp.com/api/articles?page=2",
    "results": [
        {
            "source": "Source",
            "url": "https://www.dummy.com/2022/6/5/23153012/",
            "title": "Dummy Title",
            "thumbnail": "https://abc.com/C3S3_Key_Art_EN.jpg",
            "author": "Dummy Author",
            "published_time": "2022-06-05T12:05:01Z",
            "article_link": "https://my-daily-news.herokuapp.com/api/articles/772/Dummy-Title"
        },
        ...
    ] 
}
```

- From `/api/articles/{article_id}/{slug}`:

```other
{
  "content": "
    <div class="article">
     <p>Lorem ipsum dolor sit amet, </p>
     <p>consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturi</p>
    </div>
}
```


