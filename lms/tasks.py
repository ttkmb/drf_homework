import datetime
import os

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from lms.models import Course


@shared_task
@receiver(post_save, sender=Course)
def send_mail_about_update(course_name, **kwargs):
    send_mail(
        subject='Обновление курса',
        message=f'Курс {course_name} был обновлен',
        from_email=os.getenv('EMAIL_HOST_USER'),
        recipient_list=[os.getenv('EMAIL_GUEST_USER')],
    )


@shared_task
def check_monthly_authorization():
    one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    inactive_users = get_user_model().objects.filter(last_login__lt=one_month_ago, is_active=True)
    for user in inactive_users:
        user.is_active = False
        user.save(update_fields=['is_active'])
