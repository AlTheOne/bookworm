# Generated by Django 2.1.1 on 2018-09-16 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAvatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(height_field=100, help_text='Максимальный размер 100х100', upload_to='avatar/', verbose_name='Аватарка', width_field=100)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('user', models.ForeignKey(help_text='Укажите пользователя', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Аватар',
                'verbose_name_plural': 'Аватарки',
            },
        ),
    ]
