import random
from .models import Category, Post


def category_tags(request):
    try:
        tags_mix = random.sample(
            list(Category.objects.all().values_list('id', flat=True)), 10)
        tags = Category.objects.filter(id__in=tags_mix)
    except ValueError:
        tags = None
    return {'categories': tags}


def freshest_posts(request):
    return {'freshest_posts': Post.objects.all().order_by('-created')[:3]}
