from django.db import models
from django.shortcuts import reverse

class News(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Заголовок новости')
    body = models.TextField(db_index=True, verbose_name='Содержание новости')
    published = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

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
