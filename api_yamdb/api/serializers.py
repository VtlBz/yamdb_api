from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from core.validators import (TextMaxLengthValidator,
                             YaMDbUsernameValidator,
                             YearValidator, )
from reviews.models import Comment, Category, Genre, Review, Title

User = get_user_model()

user_conf = settings.USER_CREDENTIAL_SETTINGS


class RegistrationSerializer(serializers.ModelSerializer):
    """Преобразовывает данные пользователя при регистрации."""
    queryset = User.objects.all()
    username = serializers.CharField(
        required=True,
        validators=(YaMDbUsernameValidator(),)
    )
    email = serializers.EmailField(
        required=True,
        validators=(
            TextMaxLengthValidator(
                user_conf['EMAIL_MAX_LENGTH'],
                'Длинна email не может превышать 254 символа'
            ),
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if (User.objects.filter(username=data['username']).exists()
                ^ User.objects.filter(email=data['email']).exists()):
            raise serializers.ValidationError(
                'Имя пользователя или email уже используются.'
            )
        return data


class TokenSerializer(serializers.Serializer):
    """Преобразовывает данные пользователя при получении Auth-токена."""
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=254, required=True)


class UserSerializer(serializers.ModelSerializer):
    """Преобразовывает данные пользователя при добавлении/редактировании."""
    role = serializers.ChoiceField(choices=User.Role, default=User.Role.USER)

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role',)


class CategorySerializer(serializers.ModelSerializer):
    """Преобразовывает данные модели 'Category'."""
    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(queryset=Category.objects.all(),
                            lookup='iexact',
                            message='Такой slug уже есть, придумай другой')
        ]
    )

    class Meta:
        model = Category
        lookup_field = 'slug'
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Преобразовывает данные модели 'Genre'."""
    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(queryset=Genre.objects.all(),
                            lookup='iexact',
                            message='Такой slug уже есть, придумай другой')
        ]
    )

    class Meta:
        model = Genre
        lookup_field = 'slug'
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    """
    Преобразовывает данные модели 'Title'.
    Обрабатывает GET, DELETE запросы.
    """
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, default=None)
    description = serializers.CharField(required=False)

    class Meta:
        fields = '__all__'
        model = Title


class TitlePostSerializer(TitleSerializer):
    """
    Преобразовывает данные модели 'Title'.
    Обрабатывает POST, PATCH запросы.
    """
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug',
                                         many=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug',)
    description = serializers.CharField(required=False, allow_blank=True)
    year = serializers.IntegerField(validators=(YearValidator(),))

    class Meta:
        fields = '__all__'
        model = Title

        validators = (
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('category', 'name', 'year')
            ),
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Преобразовывает данные модели 'Review'."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        model = Review
        exclude = ('title',)
        read_only_fields = ('author',)

    def validate(self, data):
        if Review.objects.filter(
            author=self.context['request'].user,
            title__id=self.context['view'].kwargs.get('title_id')
        ).exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Вы уже оставляли ревью на данное произведение. '
                'Для редактирования используйте соответствующий эндпоинт.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Преобразовывает данные модели 'Comment'."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)
        read_only_fields = ('author',)
