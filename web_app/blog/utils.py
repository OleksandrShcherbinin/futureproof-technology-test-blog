import json
from django.conf import settings
from requests_html import HTMLSession
from .models import Post


def get_proxies():
    with HTMLSession() as session:
        session.auth = (settings.APROXY_USERNAME, settings.APROXY_PASSWORD)
        proxy = session.get(url=f'{settings.APROXY_API_URL}')
        proxies = json.loads(proxy.text)
        proxies = {'http': f'{proxies}',
                   'https': f'{proxies}'}
    return proxies


def get_url_response(url, proxies):
    if proxies:
        proxies = get_proxies()
        if proxies.get('http'):
            with HTMLSession() as session:
                response = session.get(url,
                                       headers=settings.GOOGLE_BOT_HEADERS,
                                       proxies=proxies,
                                       timeout=30,
                                       )
        else:
            with HTMLSession() as session:
                response = session.get(url, timeout=30)
    else:
        with HTMLSession() as session:
            response = session.get(url, timeout=30)

    return response


def divide_in_chunks(num_list, chunk_size):

    for i in range(0, len(num_list), chunk_size):
        yield num_list[i:i + chunk_size]


def get_posts_urls(sitemap_url):
    with HTMLSession() as session:
        response = session.get(sitemap_url)
    post_sources = Post.objects.all().values_list('source', flat=True)
    posts_urls = [elem for elem in response.html.xpath('//url/loc/text()')
                  if elem not in post_sources]
    return posts_urls
