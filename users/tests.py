import pytest
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


@pytest.mark.django_db
class TestUser:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = User.objects.create(email="test@mail.ru", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_user_self(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:user_retrieve")

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["email"] == "test@mail.ru"

    def test_create_user(self):
        data = {
            "email": "new@mail.ru",
            "password": "new",
        }
        url = reverse("users:register")
        response = self.client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.all().count() == 2

    def test_reset_password(self):
        data = {
            "email": "test@mail.ru",
        }
        url = reverse("users:password_reset")
        response = self.client.post(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "detail": "Ссылка для сброса пароля отправлена на ваш email"
        }

    def test_reset_password_confirm(self):
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        data = {"uid": uid, "token": token, "new_password": "new_password"}
        url = reverse("users:password_reset_confirm")
        response = self.client.post(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"detail": "Пароль успешно изменен"}

        user = User.objects.get(email="test@mail.ru")

        assert user.check_password("new_password")
