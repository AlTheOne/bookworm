# Generated by Django 2.1.1 on 2018-09-25 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import userApp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('login', models.CharField(max_length=32, unique=True, verbose_name='login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('first_name', models.CharField(blank=True, max_length=400, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=400, null=True, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('phone_number', models.CharField(max_length=20, unique=True, verbose_name='phone number')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', userApp.models.UserAccountManager()),
            ],
        ),
        migrations.CreateModel(
            name='RecoveryPaswdlUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Рандомная строка', max_length=100, verbose_name='Код подтверждения')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('user', models.ForeignKey(help_text='Укажите пользователя', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Восстановление пароля',
                'verbose_name_plural': 'Восстановление паролей',
            },
        ),
        migrations.CreateModel(
            name='UserAvatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, help_text='Максимальный размер 100х100', null=True, upload_to='avatar/', verbose_name='Аватарка')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('user', models.OneToOneField(help_text='Укажите пользователя', on_delete=django.db.models.deletion.CASCADE, related_name='ava', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Аватар',
                'verbose_name_plural': 'Аватарки',
            },
        ),
        migrations.CreateModel(
            name='СonfirmationEmailUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Рандомная строка', max_length=100, verbose_name='Код подтверждения')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('user', models.ForeignKey(help_text='Укажите пользователя', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Подтверждение почты',
                'verbose_name_plural': 'Подтверждения почты',
            },
        ),
    ]
