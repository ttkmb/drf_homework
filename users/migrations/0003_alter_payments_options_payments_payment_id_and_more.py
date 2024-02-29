# Generated by Django 5.0.2 on 2024-02-29 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_payments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payments',
            options={'verbose_name': 'Оплата', 'verbose_name_plural': 'Платежи'},
        ),
        migrations.AddField(
            model_name='payments',
            name='payment_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ID платежа'),
        ),
        migrations.AddField(
            model_name='payments',
            name='payment_link',
            field=models.URLField(blank=True, max_length=400, null=True, verbose_name='Ссылка на оплату'),
        ),
    ]
