from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models.aggregates import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.serializers import (CategorySerializer,
                             CommentSerializer,
                             GenreSerializer,
                             RegistrationSerializer,
                             ReviewSerializer,
                             TitlePostSerializer,
                             TitleSerializer,
                             TokenSerializer,
                             UserSerializer)
from core.permissions import (AllowAny,
                              IsAuthenticated,
                              IsAuthenticatedOrReadOnly,
                              IsAdmin,
                              IsAdminOrReadOnly,
                              IsOwner,
                              IsStuff)
from reviews.models import (
    Category,
    Genre,
    Review,
    Title
)

User = get_user_model()


email_form: dict = {
    'subject': 'Код подтверждения на YaMDB',
    'message': ('Вы запросили код подтверждения в сервисе YaMDb.\n'
                'Ваш код: {}\n'
                'Не сообщайте его третьим лицам.'),
    'from_email': settings.DEFAULT_FROM_EMAIL,
}


class BaseCreateDestroyListViewSet(mixins.CreateModelMixin,
                                   mixins.DestroyModelMixin,
                                   mixins.ListModelMixin,
                                   viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class RegistrationViewAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user, is_create = User.objects.get_or_create(
            username=username, email=email,
        )
        confirmation_code = default_token_generator.make_token(user)
        user.email_user(
            subject=email_form['subject'],
            message=email_form['message'].format(confirmation_code),
            from_email=email_form['from_email'],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTokenViewAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        if default_token_generator.check_token(
                user, serializer.validated_data['confirmation_code']
        ):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['PATCH', 'GET'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def current_user_info(self, request):
        self.get_serializer()
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
        else:
            serializer = UserSerializer(request.user,
                                        data=request.data,
                                        partial=True,)
            serializer.is_valid(raise_exception=True)
            if not request.user.is_admin:
                serializer.validated_data['role'] = request.user.role
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(BaseCreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseCreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitlePostSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsStuff | IsOwner | IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsStuff | IsOwner | IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review,
                                   pk=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review,
                                   pk=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            review=review
        )
