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
    last_login = models.DateTimeField(auto_now=True, verbose_name='Последний вход', null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Payments(models.Model):
    class payment_method_choices(models.TextChoices):
        CASH = 'cash', 'Наличные'
        TRANSFER = 'transfer', 'Перевод на счет'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата платежа')
    paid_course = models.ForeignKey('lms.Course', on_delete=models.SET_NULL, verbose_name='Курс', null=True)
    paid_lesson = models.ForeignKey('lms.Lesson', on_delete=models.SET_NULL, verbose_name='Урок', null=True, blank=True)
    payment_method = models.CharField(choices=payment_method_choices.choices,
                                      verbose_name='Способ оплаты')
    payment_link = models.URLField(verbose_name='Ссылка на оплату', null=True, blank=True, max_length=400)
    payment_id = models.CharField(max_length=255, verbose_name='ID платежа', null=True, blank=True)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return self.payment_id
