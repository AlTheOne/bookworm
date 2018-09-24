# Generated by Django 2.1.1 on 2018-09-17 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0005_auto_20180917_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useravatar',
            name='user',
            field=models.ForeignKey(help_text='Укажите пользователя', on_delete=django.db.models.deletion.CASCADE, related_name='ava', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]