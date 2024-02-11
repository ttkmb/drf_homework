from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='images/', verbose_name='Превью')
    description = models.TextField(verbose_name='Описание')


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='images/', verbose_name='Превью')
    description = models.TextField(verbose_name='Описание')
    video_link = models.URLField(verbose_name='Ссылка на видео', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
