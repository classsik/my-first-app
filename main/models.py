from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

class News(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Заголовок новости')
    body = models.TextField(db_index=True, verbose_name='Содержание новости')
    published = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    image = models.ImageField(upload_to='news/%Y/%m/%d', blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name_plural = 'Новости'
        verbose_name = 'Новость'
        ordering = ['-published']

class Shedule(models.Model):
    day = models.CharField(max_length=100, db_index=True, verbose_name='День недели')
    lesson1 = models.CharField(max_length=100, db_index=True, verbose_name='Урок 1')
    lesson2 = models.CharField(max_length=100, db_index=True, verbose_name='Урок 2')
    lesson3 = models.CharField(max_length=100, db_index=True, verbose_name='Урок 3')
    lesson4 = models.CharField(max_length=100, db_index=True, verbose_name='Урок 4')
    lesson5 = models.CharField(max_length=100, db_index=True, verbose_name='Урок 5')
    lesson6 = models.CharField(max_length=100, db_index=True, verbose_name='Урок 6')
    lesson7 = models.CharField(max_length=100, db_index=True, verbose_name='Урок 7')

    def __str__(self):
        return self.day

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

class Comment(models.Model):
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    name = models.ForeignKey(User, related_name='name', on_delete=models.PROTECT, verbose_name='Автор')
    body = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    active = models.BooleanField(default=True, verbose_name='Активный?')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.news)

class Call(models.Model):
    lesson = models.IntegerField(verbose_name='Урок', default='1')
    start = models.TimeField(verbose_name='Время начала')
    end = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Расписание звонков'
        verbose_name_plural = 'Расписание звонков'

    def __str__(self):
        return 'Call on {} lesson'.format(self.lesson)

class Subject(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название предмета')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Слаг')
    class Meta:
        ordering = ['title']
        verbose_name='Предмет'
        verbose_name_plural='Предметы'

    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE, verbose_name='Автор')
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE, verbose_name='Предмет')
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Слаг')
    overview = models.TextField(verbose_name='Описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)
    class Meta:
        ordering = ['-created']
        verbose_name='Курс'
        verbose_name_plural='Курсы'

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE, verbose_name='Курс')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    order = OrderField(blank=True, for_fields=['course'])
    def __str__(self):
        return '{}. {}'.format(self.order, self.title)
    class Meta:
        verbose_name='Модуль'
        verbose_name_plural='Модули'
        ordering = ['order']


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE, verbose_name='Модуль')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in':('text', 'video', 'image', 'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])
    class Meta:
        verbose_name='Контент'
        verbose_name_plural='Контент'
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=250, verbose_name='Название')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string('courses/content/{}.html'.format(self._meta.model_name), {'item': self}) 

class Text(ItemBase):
    content = models.TextField(verbose_name='Содержание')

class File(ItemBase):
    file = models.FileField(upload_to='files', verbose_name='Файл')
class Image(ItemBase):
    file = models.FileField(upload_to='images', verbose_name='Изображение')

class Video(ItemBase):
    url = models.URLField(verbose_name='URL Видео')
