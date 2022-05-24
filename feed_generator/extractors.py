import datetime
import re
import time
from urllib.parse import urljoin

import bs4
import feedparser
import requests
from api.models import Article, Source
from django.conf import settings
from django.db import utils

from feed_generator.content_extractor import Content_Extractor

REQUEST_ARTICLE_TIMEOUT = settings.REQUEST_ARTICLE_TIMEOUT


def download_article(url):
    """
    Download data from page and convert to BeautifulSoup object
    """
    try: 
        response = requests.get(url,timeout = REQUEST_ARTICLE_TIMEOUT) 
    except requests.exceptions.Timeout:
        pass
    else:
        if response.ok:
            return bs4.BeautifulSoup(response.content, features="lxml")
    return ''

def get_thumbnail(html, url):
    """
    Get thumbnail of the article
    """
    if not html:
        return ''
    value = 'og:image'
    img_of_content_url = ''
    for attr in ['property', 'name']:
        matched_tag = html.find('meta', attrs={attr: value})
        if matched_tag:
            img_of_content_url = matched_tag.attrs['content']
            break
    if not img_of_content_url:
        value = re.compile(r'img_src')
        matched_tag = html.find('link', attrs={'rel': value})
        if matched_tag:
            img_of_content_url = matched_tag.attrs['href']
    if img_of_content_url:
        return urljoin(url, img_of_content_url)
    return ''



def get_content(html, url):
    """
    Extract main content of the article
    """

    if not html:
        print('No HTML')
        return ''
    def clean_tags(html):
        # Unwrap tags
        merging_tags = ['li', 'table', 'tbody', 'tr', 'td',
                        'theader', 'tfoot', 'em', 'strong', 'i', 'u', 'b']
        tags = html.find_all(merging_tags)
        for tag in tags:
            tag.unwrap()

        for tag in html.find_all('p'):
            tag.append(html.new_tag('br'))
            tag.unwrap()

        # Remove tags:
        remove_tag = ['head', 'script', 'link', 'style', 'form',
                      'option', 'header', 'footer', 'nav', 'noscript', 'aside']
        tags = html.find_all(remove_tag)
        for tag in tags:
            tag.decompose()

        # Remove hidden tags:
        for hidden in html.find_all(style=re.compile(r'display:\s*none')):
            hidden.decompose()

        return html
    cleaned_html = clean_tags(html)

    body = cleaned_html.find('body')
    extractor = Content_Extractor.create(body)
    best_node = extractor.extract()


    def get_img(tag):
        img_pattern = re.compile(r'\/.+(jpg|jpeg|png|webp)')
        attrs_check = ['data-original', 'src',
                        'srcset', 'data-src', 'data-srcset']
        found = []
        img_name = []
        img_url = []

        for att in attrs_check:
            for t in tag.find_all(attrs={att: img_pattern}):
                found.append(t.attrs[att])
        for n in found:
            name = re.sub('\s.+', '', n.split('/')[-1])
            if name not in img_name:
                img_name.append(name)
                img_url.append(n)
        return img_url

    def get_img_tag(node, url):
        img_url = get_img(node)
        if not img_url:
            return ''
        img_url = urljoin(url, img_url[0])
        cite = []
        for i in node.descendants:
            if i != '\n' and isinstance(i, bs4.element.NavigableString):
                cite.append(i)

        figcaption = ''

        for c in cite:
            figcaption = figcaption + c + ' '

        tag = '<figure><img src="' + img_url + '" alt=""><figcaption>' + figcaption + '</figcaption></figure>'
        return tag

    children = list(best_node.soup.children)
    article_list = []
    while children:
        next_child = []
        group_text = ''
        for i in range(len(children)):
            if children[i] == '\n':
                if group_text:
                    # count += 1
                    # if group_text[0] != '<' and group_text[-1] != '>':
                    group_text = '<p>' + group_text + '</p>'
                    article_list.append(group_text)
                    group_text = ''

            elif isinstance(children[i], bs4.element.NavigableString):
                group_text += children[i] + ' '

            elif children[i].name == 'br':
                # group_text += str(children[i])
                pass

            elif children[i].name in ['a', 'blockquote', 'p', 'span', 'code', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                group_text += str(children[i])

            elif children[i].name in ['figure', 'img', 'picture']:
                group_text += get_img_tag(children[i], url)

            elif children[i].name in ['audio', 'video', 'footer', 'iframe']:
                pass

            else:
                next_child.extend(list(children[i].children))
                next_child.extend(children[i+1:])
                break
        if group_text:
            article_list.append(group_text)
        children = next_child

    joined_articles = ''.join(article_list)
    soup = bs4.BeautifulSoup(
        '<div class="article">' + joined_articles + '</div>', 'lxml')
    content = soup.find('div', attrs={'class': 'article'})
    return str(content)

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
            published_time = datetime.datetime.utcfromtimestamp(time.mktime(entry.published_parsed))
            thumbnail = ''
            content = ''
            html = download_article(url)
            is_scraping = True
            if html:
                thumbnail = get_thumbnail(html, url)
                content = get_content(html, url)
                if content:
                    is_scraping = False


            # Save article to database if it is not exist
            try: 
                Article.objects.get_or_create(
                    url = url,
                    defaults={
                        'from_source': source,
                        'topic_id': 1,
                        'author': author,
                        'title': title,
                        'published_time': published_time,
                        'content': content,
                        'thumbnail': thumbnail,
                        'is_scraping': is_scraping,
                    }
                )
            except utils.DataError:
                # TODO handle article that has too long value field
                pass
