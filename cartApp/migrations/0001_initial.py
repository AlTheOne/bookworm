# Generated by Django 2.1.1 on 2018-09-25 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=256, verbose_name='ID сессии')),
                ('object_id', models.PositiveIntegerField(help_text='ID объекта указанной модели', verbose_name='ID объекта')),
                ('count', models.PositiveIntegerField(default=1, help_text='Не менее одного', verbose_name='Количество')),
                ('is_active', models.BooleanField(default=True, help_text='Видно пользователям, только если активно', verbose_name='Активно')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('content_type', models.ForeignKey(help_text='Выберите модель', on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='Модель')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete='SET_NULL', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
    ]
