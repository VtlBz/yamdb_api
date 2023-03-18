# Generated by Django 3.2.16 on 2022-12-24 11:50

import core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название категории', max_length=256, verbose_name='Название категории')),
                ('slug', models.SlugField(help_text='Укажите идентификатор (slug) для категории. Используйте только латиницу, цифры, дефисы и знаки подчёркивания', unique=True, verbose_name='Идентификатор (slug) категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'db_table': 'categories',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Текст комментария', verbose_name='Текст комментария')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Дата публикации комментария', verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'db_table': 'comments',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название жанра', max_length=256, verbose_name='Название жанра')),
                ('slug', models.SlugField(help_text='Укажите идентификатор (slug)  для жанра. Используйте только латиницу, цифры, дефисы и знаки подчёркивания', unique=True, verbose_name='Идентификатор (slug) жанра')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'db_table': 'genres',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Текст отзыва', verbose_name='Текст отзыва')),
                ('score', models.PositiveIntegerField(choices=[(10, '10 - Потрясающе'), (9, '9 - Превосходно'), (8, '8 - Очень хорошо'), (7, '7 - Хорошо'), (6, '6 - Удовлетворительно'), (5, '5 - Посредственно'), (4, '4 - Плохо'), (3, '3 - Очень плохо'), (2, '2 - Ужасно'), (1, '1 - Полный провал')], help_text='Оценка произведения', null=True, verbose_name='Оценка')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Дата публикации отзыва', verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'db_table': 'reviews',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Название произведения', max_length=256, verbose_name='Название')),
                ('year', models.IntegerField(db_index=True, help_text='Год выпуска произведения', validators=[core.validators.YearValidator()], verbose_name='Год выпуска')),
                ('description', models.TextField(blank=True, help_text='Описание произведения', verbose_name='Описание произведения')),
                ('category', models.ForeignKey(blank=True, help_text='Категория произведения', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(help_text='Жанр произведения', related_name='titles', to='reviews.Genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'db_table': 'titles',
                'ordering': ('pk',),
            },
        ),
    ]
