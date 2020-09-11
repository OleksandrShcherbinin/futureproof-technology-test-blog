from django.db import models
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=100, unique=True)

    objects = models.Manager()

    def get_absolute_url(self):
        return f'/category/{self.slug}'

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)

    objects = models.Manager()

    def get_absolute_url(self):
        return f'/author/{self.slug}'

    def __str__(self):
        return self.name


class Post(models.Model):
    class Meta:
        ordering = ["-published"]

    title = models.CharField(
        max_length=255,
        verbose_name='post title')
    slug = models.SlugField(
        max_length=300,
        unique=True)
    source = models.URLField(
        max_length=1024,
        blank=True, null=True)
    image = models.ImageField(
        upload_to='images',
        verbose_name='main post image')
    created = models.DateTimeField(
        verbose_name='datetime of post creation')
    moderated = models.BooleanField(
        default=False,
        verbose_name='post allowed to publish')
    published = models.DateTimeField(
        blank=True, null=True,
        verbose_name='datetime when post was published')
    last_update = models.DateTimeField(auto_now=True)
    content = models.TextField(verbose_name='post full text')

    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                               related_name='post_author')

    category = models.ManyToManyField(Category)

    objects = models.Manager()

    def get_absolute_url(self):
        return f'/{self.slug}'

    def __str__(self):
        return self.title


class Subscribe(models.Model):
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True,
                                verbose_name='datetime of email subscription')

    objects = models.Manager()

    def save(self, *args, **kwargs):
        subject = 'Thank you for subscribing No-Chaos'
        from_email = settings.EMAIL_HOST_USER
        to = self.email
        text_content = 'Dear friend! Thank you for subscribing our blog'
        with open(settings.BASE_DIR + '/templates/email.html') as template:
            html_content = template.read()
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        super(Subscribe, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
