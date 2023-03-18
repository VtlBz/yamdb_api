from typing import Tuple

from django.contrib.auth import get_user_model
from django.db import models

from core.validators import YearValidator

User = get_user_model()


class Category(models.Model):
    """Категории (типы) произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
        help_text='Введите название категории',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Идентификатор (slug) категории',
        help_text='Укажите идентификатор (slug) для категории. '
                  'Используйте только латиницу, цифры, дефисы '
                  'и знаки подчёркивания',
        db_index=True,
    )

    class Meta:
        db_table = 'categories'
        ordering = ('pk',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
        help_text='Введите название жанра',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Идентификатор (slug) жанра',
        help_text='Укажите идентификатор (slug)  для жанра. '
                  'Используйте только латиницу, цифры, дефисы '
                  'и знаки подчёркивания',
        db_index=True,
    )

    class Meta:
        db_table = 'genres'
        ordering = ('pk',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения добавленные в БД."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Название произведения',
        db_index=True,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        help_text='Год выпуска произведения',
        db_index=True,
        validators=(YearValidator(),),
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        help_text='Категория произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Жанр произведения',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание произведения',
        help_text='Описание произведения',
    )

    class Meta:
        db_table = 'titles'
        ordering = ('pk',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [models.UniqueConstraint(
            fields=['category', 'name', 'year'],
            name='unique_title')
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы оставленные к произведению."""
    class Score(models.IntegerChoices):
        AWESOME: Tuple[int, str] = (10, '10 - Потрясающе',)
        EXCELLENT: Tuple[int, str] = (9, '9 - Превосходно',)
        VERY_GOOD: Tuple[int, str] = (8, '8 - Очень хорошо',)
        GOOD: Tuple[int, str] = (7, '7 - Хорошо',)
        SATISFACTORY: Tuple[int, str] = (6, '6 - Удовлетворительно',)
        MEDIOCRE: Tuple[int, str] = (5, '5 - Посредственно',)
        BAD: Tuple[int, str] = (4, '4 - Плохо',)
        VERY_BAD: Tuple[int, str] = (3, '3 - Очень плохо',)
        DREADFUL: Tuple[int, str] = (2, '2 - Ужасно',)
        EPIC_FAIL: Tuple[int, str] = (1, '1 - Полный провал',)

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Произведение, к которому оставлен отзыв',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Текст отзыва',
    )
    score = models.PositiveIntegerField(
        null=True,
        choices=Score.choices,
        verbose_name='Оценка',
        help_text='Оценка произведения',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        help_text='Автор отзыва',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата публикации отзыва',
    )

    class Meta:
        db_table = 'reviews'
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [models.UniqueConstraint(
            fields=('author', 'title',),
            name='unique_review')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии к отзывам"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв, к которому оставлен комментарий',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата публикации комментария',
    )

    class Meta:
        db_table = 'comments'
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
