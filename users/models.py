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


class Payments(models.Model):
    class payment_method_choices(models.TextChoices):
        CASH = 'cash', 'Наличные'
        TRANSFER = 'transfer', 'Перевод на счет'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    amount = models.FloatField(verbose_name='Сумма оплаты')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата платежа')
    paid_course = models.ForeignKey('lms.Course', on_delete=models.SET_NULL, verbose_name='Курс', null=True, blank=True)
    paid_lesson = models.ForeignKey('lms.Lesson', on_delete=models.SET_NULL, verbose_name='Урок', null=True, blank=True)
    payment_method = models.CharField(choices=payment_method_choices.choices,
                                      verbose_name='Способ оплаты')
