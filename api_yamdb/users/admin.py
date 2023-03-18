from django.contrib import admin
from django.contrib.auth import get_user_model

from import_export import resources
from import_export.admin import ImportExportModelAdmin

User = get_user_model()


class UserResource(resources.ModelResource):
    """Настраивает модель импорта-экспорта через админ-зону ресурса."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'bio',
        )


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    """Настраивает модель отображения данных в админ-зоне ресурса."""
    resource_class = UserResource
    list_display = (
        'pk', 'username', 'email', 'first_name', 'last_name', 'last_login',
        'role', 'is_active', 'is_staff', 'is_superuser',
    )
    list_editable = ('role',)
    search_fields = (
        'pk', 'username', 'email', 'first_name', 'last_name', 'bio',
    )
    list_filter = ('role', 'last_login', 'date_joined',)
