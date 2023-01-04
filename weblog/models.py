from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.html import format_html


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)

# Create your models here.


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name='زیردسته')
    title = models.CharField(max_length=100, verbose_name='عنوان دسته‌بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس دسته‌بندی')
    status = models.BooleanField(default=True, verbose_name='وضعیت نمایش')
    position = models.IntegerField(verbose_name='جایگاه')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی ها"
        ordering = ('parent__id', 'position',)

    objects = CategoryManager()


class Article(models.Model):
    STATUS_CHOICES = (
        ('p', 'منتشر شده'),
        ('d', 'پیش‌نویس')
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='article', verbose_name="نویسنده")
    title = models.CharField(max_length=100, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس مقاله')
    category = models.ManyToManyField(Category, related_name='article',)
    description = models.TextField(verbose_name='محتوا')
    thumbnail = models.ImageField(upload_to='images', verbose_name='تصویر مقاله')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضیعت انتشار')

    def __str__(self):
        return '{}- {}'.format(self.id, self.title)

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ('-publish',)

    def cat_pub(self):
        return self.category.filter(status=True)

    def get_absolute_url(self):
        return reverse('account:home')

    def thumbnail_tag(self):
        return format_html("<img width='100' height='75' src='{}'>".format(self.thumbnail.url))

    def categories(self):
        return ", ".join(category.title for category in self.category.active())
    categories.short_description = 'دسته‌بندی ها'

    objects = ArticleManager()
