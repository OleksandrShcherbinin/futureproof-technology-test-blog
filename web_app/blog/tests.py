from string import ascii_letters
from django.test import TestCase
from django.utils import timezone
from .models import Category, Post, Author


class PostModelTest(TestCase):

    def setUp(self):
        self.author = Author.objects.create(name='Test Author',
                                            slug='test-author')
        self.post = Post.objects.create(
            title='Test title',
            slug='test-slug',
            source='https://test-source.com',
            image='test-image-name.jpg',
            created=timezone.localdate(),
            moderated=True,
            published=timezone.localdate(),
            last_update=timezone.localdate(),
            content=' '.join([char for char in ascii_letters]),
            author=self.author,
            )

    # Test field label

    def test_post_title_label(self):
        field_label = self.post._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'post title')

    def test_post_slug_label(self):
        field_label = self.post._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'slug')

    def test_post_source_label(self):
        field_label = self.post._meta.get_field('source').verbose_name
        self.assertEquals(field_label, 'source')

    def test_post_image_label(self):
        field_label = self.post._meta.get_field('image').verbose_name
        self.assertEquals(field_label, 'main post image')

    def test_post_created_label(self):
        field_label = self.post._meta.get_field('created').verbose_name
        self.assertEquals(field_label, 'datetime of post creation')

    def test_post_moderated_label(self):
        field_label = self.post._meta.get_field('moderated').verbose_name
        self.assertEquals(field_label, 'post allowed to publish')

    def test_post_published_label(self):
        field_label = self.post._meta.get_field('published').verbose_name
        self.assertEquals(field_label, 'datetime when post was published')

    def test_post_last_update_label(self):
        field_label = self.post._meta.get_field('last_update').verbose_name
        self.assertEquals(field_label, 'last update')

    def test_post_content_label(self):
        field_label = self.post._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'post full text')

    def test_title_value(self):
        field_value = self.post.title
        self.assertEquals(field_value, 'Test title')

    def test_slug_value(self):
        field_value = self.post.slug
        self.assertEquals(field_value, 'test-slug')

    def test_source_value(self):
        field_value = self.post.source
        self.assertEquals(field_value, 'https://test-source.com')

    def test_image_value(self):
        field_value = self.post.image
        self.assertEquals(field_value, 'test-image-name.jpg')

    def test_created_value(self):
        field_value = self.post.created
        self.assertEquals(field_value, timezone.localdate())

    def test_moderated_value(self):
        field_value = self.post.moderated
        self.assertEquals(field_value, True)

    def test_published_value(self):
        field_value = self.post.published
        self.assertEquals(field_value, timezone.localdate())

    def test_last_update_value(self):
        field_value = self.post.last_update
        self.assertEqual(field_value.date(), timezone.now().date())

    def test_content_value(self):
        field_value = self.post.content
        self.assertEquals(field_value, ' '.join([char for char in ascii_letters]))


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='TestCategory',
                                                slug='test-category',
                                                )

    # Test field label
    def test_name_label(self):
        field_label = self.category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_slug_label(self):
        field_label = self.category._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'slug')

    # Test field value
    def test_name_value(self):
        field_value = self.category.name
        self.assertEquals(field_value, 'TestCategory')

    def test_slug_value(self):
        field_value = self.category.slug
        self.assertEquals(field_value, 'test-category')


class AuthorModelTest(TestCase):

    def setUp(self):
        self.author = Author.objects.create(name='Test Author',
                                            slug='test-author',
                                            )

    # Test field label
    def test_name_label(self):
        field_label = self.author._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_slug_label(self):
        field_label = self.author._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'slug')

    # Test field value
    def test_name_value(self):
        field_value = self.author.name
        self.assertEquals(field_value, 'Test Author')

    def test_slug_value(self):
        field_value = self.author.slug
        self.assertEquals(field_value, 'test-author')
