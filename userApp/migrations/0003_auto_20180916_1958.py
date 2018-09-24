# Generated by Django 2.1.1 on 2018-09-16 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0002_useravatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useravatar',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, height_field=100, help_text='Максимальный размер 100х100', null=True, upload_to='avatar/', verbose_name='Аватарка', width_field=100),
        ),
        migrations.DeleteModel(
            name='UserAvatar',
        ),
    ]