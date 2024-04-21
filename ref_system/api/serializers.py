from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from users.models import CustomUserModel
from djoser.serializers import TokenCreateSerializer
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, NotFound


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализатор для регистрации польвателя.
    Переопределение входных данных для сохранения в БД в единном формате.
    """
    telephone_number = PhoneNumberField(region='RU')

    class Meta:
        model = CustomUserModel
        fields = ('telephone_number', 'confirmation_code')

    from users.utils import create_confirmation_code

    def validate(self, data):
        """ Валидация поля telephone_number. """
        if not data:
            raise ValidationError('необходимо ввести номер телефона.')
        return data


class LoginUserSerializer(TokenCreateSerializer):
    """
    Сериализатор для работы с сущностью авторизации пользователя.
    Реализовано:
        Переопределение входных данных для входа получения токена.
        Валидация краевых случаев.
    """
    confirmation_code = serializers.CharField(required=False)

    def validate(self, data):
        """ Валидация поля telephone_number. """
        confirmation_code = data.get('confirmation_code', None)
        telephone_number = data.get('telephone_number',)
        data['telephone_number'] = '+7' + telephone_number[-10:]
        try:
            user = CustomUserModel.objects.get(
                telephone_number=data['telephone_number']
            )
        except Exception:
            raise AuthenticationFailed(
                {'telephone_number':
                    'Номер не зарегестрирован в системе.'}
            )
        if confirmation_code:
            if user.confirmation_code != confirmation_code:
                raise AuthenticationFailed(
                    {'confirmation_code':
                        'неверый проверочный код.'}
                )
            data['confirmation_code'] = confirmation_code
        else:
            raise AuthenticationFailed(
                {'confirmation_code':
                    'Необходимо ввести ранее полученный проверочный код.'}
            )
        return data


class AddInvationCodeToProfile(serializers.ModelSerializer):
    """
    Сериализатор для работы добавления
    invite_code (кода пригласившего пользователя).
    Реализован валидация краевых случаев.
    """
    invitation_code = serializers.CharField(min_length=6, max_length=6)

    class Meta:
        model = CustomUserModel
        fields = ['invitation_code']

    def validate_invitation_code(self, data):
        if not data or data == self.context['request'].user.user_referal_code:
            raise ValidationError(
                'Необходимо указать реферальный код пригласившего пользователя'
                )
        try:
            CustomUserModel.objects.get(user_referal_code=data)
        except Exception:
            raise NotFound('Указанный реферальный код не существует')
        return data

    def update(self, instance, validated_data):
        invitation_code = validated_data.get('invitation_code', None)
        if instance.invitation_code:
            raise PermissionDenied('Вы уже указали код приглашения')
        instance.invitation_code = invitation_code
        instance.save()
        return instance


class ReferralSerializer(serializers.ModelSerializer):
    """ Промежуточный сериализатор для получения объектов реферралов. """
    class Meta:
        model = CustomUserModel
        fields = ['telephone_number']


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения объекта пользователя.
    Определено новое поле для отображения списка пользователей реферраллов.
    """

    all_referals = serializers.SerializerMethodField()

    class Meta:
        model = CustomUserModel
        fields = [
            'reg_data',
            'telephone_number',
            'user_referal_code',
            'all_referals'
        ]

    def get_all_referals(self, obj):
        all_referals = CustomUserModel.objects.filter(
            invitation_code=obj.user_referal_code
        )
        referral_serializer = ReferralSerializer(all_referals, many=True)
        return referral_serializer.data
