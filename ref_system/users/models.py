from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер.
    Переопределение логики создания пользователей.
    """
    def create_user(self, telephone_number, password=None, **extra_fields):
        """
        Создает и сохраняет нового пользователя
        с указанным номером телефона.
        """
        if not telephone_number:
            raise ValueError('Необходимо указать моб. номер телефона.')
        user = self.model(telephone_number=telephone_number)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telephone_number, password):
        """
        Создает и сохраняет нового суперпользователя
        с указанным номером телефона, паролем.
        """
        user = self.create_user(
            telephone_number=telephone_number,
            password=password,
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    telephone_number = PhoneNumberField(
        _('номер телефона'),
        unique=True,
        region='RU',
    )
    reg_data = models.DateField(
        _('Зарегестрирован в системе'),
        auto_now_add=True
    )
    confirmation_code = models.CharField(
        _('Код потверждения'),
        max_length=4,
        null=True,
        blank=True,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_referal_code = models.CharField(
        _('Реферальный идентификатор пользователя'),
        max_length=6,
        null=True
    )
    invitation_code = models.CharField(
        _('Реферальный идентификатор пригласившего пользователя'),
        max_length=6,
        null=True,
        blank=True
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'telephone_number'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f'{self.telephone_number}'
