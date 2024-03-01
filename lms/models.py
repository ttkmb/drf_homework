from django.conf import settings
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='images/', verbose_name='Превью', null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='course', null=True,
                              blank=True, verbose_name='Владелец')


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='images/', verbose_name='Превью', null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    video_link = models.URLField(verbose_name='Ссылка на видео', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='course')
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='lesson', null=True,
                              blank=True, verbose_name='Владелец'
                              )


class Subscription(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='user_sub')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='course_sub')
    date_subscription = models.DateField(auto_now_add=True, verbose_name='Дата подписки')
