import logging

from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView

from .models import *
from .forms import SubscribeForm

logger = logging.getLogger(__name__)


class IndexView(FormView, ListView):
    template_name = 'index.html'
    model = Post
    paginate_by = 10
    slug_field = 'slug'
    form_class = SubscribeForm
    success_url = '/'

    def get_queryset(self):
        tag = self.request.GET.get('tag')
        if tag:
            return Post.objects.filter(
                category__slug=tag,
                moderated=True).select_related('author').order_by('-created')
        return Post.objects.filter(
            moderated=True).select_related('author').order_by('-created')

    def form_valid(self, form):
        Subscribe.objects.create(**form.cleaned_data)
        messages.add_message(self.request, messages.INFO, "Thank you!")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(form)
        messages.add_message(self.request, messages.INFO,
                             'Form filled incorrectly!')
        return super().form_invalid(form)


class PostView(DetailView):
    template_name = 'single-blog.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = self.object.category.all()
        return context

