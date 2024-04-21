from api.serializers import (RegistrationSerializer, LoginUserSerializer,
                             AddInvationCodeToProfile, ProfileSerializer)
from rest_framework import status
from rest_framework.response import Response
from users.models import CustomUserModel
from users.utils import create_confirmation_code, generate_referal_code
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class RegistationViewSet(viewsets.GenericViewSet, CreateModelMixin):
    """
    Вью регистрации пользователя в системе
    с последующей отправкой кода потверждения для входа.
    Если пользователя нет в базе он создается,
    если есть - генерируется и сохраняется в БД новый код потверждения.
    """
    serializer_class = RegistrationSerializer
    model = CustomUserModel

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        existing_user = CustomUserModel.objects.filter(
            telephone_number=serializer.validated_data['telephone_number']
        ).first()
        if existing_user:
            existing_user.confirmation_code = create_confirmation_code()
            existing_user.save()
            return Response(
                {'confirmation_code': existing_user.confirmation_code},
                status=status.HTTP_201_CREATED
            )
        else:
            user = serializer.save()
            user.confirmation_code = create_confirmation_code()
            user.save()
            return Response(
                {'confirmation_code': user.confirmation_code},
                status=status.HTTP_200_OK
            )


class LoginUserView(APIView):
    """
    Вью для получения токена из БД.
    Пользователь проверяется в базе по номеру телефона,
    затем по совпадению переданного кода и кода из БД.
    При успехе возвращается токен.

    Добавлена функциональность после 1 авторизации генерируется
    индивидуальный реферальный код, который храниться в БД.
    """
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUserModel.objects.get(
            telephone_number=serializer.validated_data['telephone_number']
        )
        user.is_active = True
        if not user.user_referal_code:
            user.user_referal_code = generate_referal_code()
        user.save()
        token = Token.objects.get_or_create(user=user)[0]
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class ProfileViewSet(
    viewsets.GenericViewSet,
    RetrieveModelMixin,
    UpdateModelMixin
):
    """
    Вью работающее с полями пользователя.
    Обрабатывает GET для получения объекта пользователя.
    Обрабатывает PUT, PATCH для внесения инвайт кода в свой профиль,
    пригласившего его пользователя.
    """
    queryset = CustomUserModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'telephone_number'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProfileSerializer
        elif self.action == 'update':
            return AddInvationCodeToProfile
        else:
            raise NotImplementedError

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user:
            raise PermissionDenied(
                'Вы не можете обновлять профиль другого пользователя'
            )
        return super().update(request, *args, **kwargs)
