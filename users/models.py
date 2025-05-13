from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    USER = "Пользователь"
    ADMIN = "Администратор"

    ROLE_CHOICES = [
        (USER, "Пользователь"),
        (ADMIN, "Администратор"),
    ]

    username = None
    first_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Имя пользователя"
    )
    last_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Фамилия пользователя"
    )
    phone = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите Email"
    )
    role = models.CharField(
        default=USER, choices=ROLE_CHOICES, verbose_name="Роль пользователя"
    )
    image = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите свой аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
