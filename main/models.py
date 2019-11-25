from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

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
