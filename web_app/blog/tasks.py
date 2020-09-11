import os
import sys
import logging
from time import sleep
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from futureproof import celery_app
from celery.result import AsyncResult
from slugify import slugify
from requests_html import HTMLSession
from django_celery_results.models import TaskResult

from .utils import get_url_response, divide_in_chunks, get_posts_urls
from .models import *

logger = logging.getLogger('parser')

TASK_KWARGS = {
    'autoretry_for': (Exception, ),
    'retry_kwargs': {'max_retries': 10000},
    'default_retry_delay': 2
}


@celery_app.task(**TASK_KWARGS)
def get_one_post(url, proxies):

    response = get_url_response(url, proxies)
    if response.status_code == 404:
        del response, proxies, url
        return 'No such page on website!'

    assert response.status_code == 200

    title = response.html.xpath('//h1')[0].text
    author = response.html.xpath('//div[@class="td-post-author-name"]/a')[0].text
    date = response.html.xpath('//time')[0].text
    created_date = timezone.make_aware(datetime.strptime(date, '%b %d, %Y'))

    content = [f'<p>{elem.text}</p>' for elem in
               response.html.xpath('//div[@class="td-post-content"]/p')]
    tags = [elem.text for elem in
            response.html.xpath('//div[@class="td-post-source-tags"]//li')][1:]

    try:
        image = response.html.xpath(
            '//div[@class="td-post-featured-image"]//img/@src')
        with HTMLSession() as session2:
            resp_img = session2.get(image[0])
            image_name = 'images/' + image[0].split("/")[-1]
        with open(os.path.join(settings.BASE_DIR,
                               f'media/{image_name}'), 'wb') as picture:
            picture.write(resp_img.content)
        del resp_img
    except Exception as e:
        logger.info(e, sys.exc_info()[-1].tb_lineno)
        image_name = 'images/default.jpg'
    author, created = Author.objects.get_or_create(name=author,
                                                   slug=slugify(author)
                                                   )
    article = {
        'title': title,
        'slug': slugify(title),
        'source': url,
        'image': image_name,
        'created': created_date,
        'content': '\n'.join(content),
        'author': author
    }

    post, created = Post.objects.get_or_create(**article)

    for tag in tags:
        cat, created = Category.objects.get_or_create(name=tag,
                                                      slug=slugify(tag)
                                                      )
        post.category.add(cat)


@celery_app.task
def get_posts(sitemap_url='https://www.thetravelmagazine.net/post-sitemap2.xml',
              proxies=True, chunk_size=20):

    tasks_set = set()
    post_urls = get_posts_urls(sitemap_url)
    chunks = divide_in_chunks(post_urls, chunk_size)

    for chunk in chunks:
        for url in chunk:
            run_task = get_one_post.delay(url, proxies)
            tasks_set.add(run_task.id)

        # wait for tasks of one chunk of urls to complete
        while len(tasks_set) != 0:
            for task_id in tasks_set.copy():
                result = AsyncResult(task_id)
                if result.state == 'SUCCESS' or result.state == 'FAILURE':
                    tasks_set.remove(task_id)
            sleep(20)


@celery_app.task
def clean_task_results_all():
    TaskResult.objects.all().exclude(status='FAILURE').delete()


