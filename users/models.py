from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=150, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='Фамилия')
    email = models.EmailField(blank=True, verbose_name='E-mail', null=True, unique=True)
    phone = PhoneNumberField(blank=True, verbose_name='Телефон', null=True)
    city = models.CharField(max_length=150, blank=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='images', blank=True, verbose_name='Аватар', null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


