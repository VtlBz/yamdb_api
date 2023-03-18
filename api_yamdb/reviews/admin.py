from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import DateTimeWidget
from reviews.models import Category, Comment, Genre, Review, Title

DEFAULT_FOR_EMPTY: str = '-empty-'


class CategoryResource(resources.ModelResource):
    """Настраивает модель импорта-экспорта через админ-зону ресурса."""
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug',)


class GenreResource(resources.ModelResource):
    """Настраивает модель импорта-экспорта через админ-зону ресурса."""
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug',)


class TitleResource(resources.ModelResource):
    """Настраивает модель импорта-экспорта через админ-зону ресурса."""
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category',)


class ReviewResource(resources.ModelResource):
    """Настраивает модель импорта-экспорта через админ-зону ресурса."""
    pub_date = Field(widget=DateTimeWidget("%Y-%m-%dT%H:%M:%S.%fZ"),
                     attribute='pub_date',
                     column_name='pub_date')

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'score', 'author', 'pub_date',)


class CommentResource(resources.ModelResource):
    """Настраивает модель импорта-экспорта через админ-зону ресурса."""
    pub_date = Field(widget=DateTimeWidget("%Y-%m-%dT%H:%M:%S.%fZ"),
                     attribute='pub_date',
                     column_name='pub_date')

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date',)


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    """Настраивает модель отображения данных в админ-зоне ресурса."""
    resource_class = CategoryResource
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('pk', 'name', 'slug',)
    empty_value_display = DEFAULT_FOR_EMPTY


@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    """Настраивает модель отображения данных в админ-зоне ресурса."""
    resource_class = GenreResource
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('pk', 'name', 'slug',)
    empty_value_display = DEFAULT_FOR_EMPTY


@admin.register(Title)
class TitleAdmin(ImportExportModelAdmin):
    """Настраивает модель отображения данных в админ-зоне ресурса."""
    resource_class = TitleResource
    list_display = ('pk', 'name', 'year', 'category', 'description',)
    search_fields = ('pk', 'name', 'description',)
    list_filter = ('category', 'genre', 'year',)
    empty_value_display = DEFAULT_FOR_EMPTY


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    """Настраивает модель отображения данных в админ-зоне ресурса."""
    resource_class = ReviewResource
    list_display = ('pk', 'title', 'text', 'score', 'author', 'pub_date',)
    search_fields = ('pk', 'title', 'text', 'score', 'author', 'pub_date',)
    list_filter = ('author', 'score', 'pub_date',)
    empty_value_display = DEFAULT_FOR_EMPTY


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    """Настраивает модель отображения данных в админ-зоне ресурса."""
    resource_class = CommentResource
    list_display = ('pk', 'review', 'text', 'author', 'pub_date',)
    search_fields = ('pk', 'review', 'text', 'author', 'pub_date',)
    list_filter = ('author', 'review', 'pub_date',)
    empty_value_display = DEFAULT_FOR_EMPTY
