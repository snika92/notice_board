import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User

from .models import Advertisement, Comment


@pytest.mark.django_db
class TestAdvertisement:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(email="user1@mail.ru", password="test")
        self.user2 = User.objects.create_user(email="user2@mail.ru", password="test")

        self.ad1 = Advertisement.objects.create(
            title="Ad 1", price=100, author=self.user1
        )
        self.ad2 = Advertisement.objects.create(
            title="Ad 2", price=200, author=self.user2
        )

    def test_create_ad_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "title": "Цветок",
            "price": 200,
        }
        url = reverse("advertisements:advertisement_create")
        response = self.client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Advertisement.objects.all().count() == 3

        ad = Advertisement.objects.get(title="Цветок")

        assert ad.author == self.user1

    def test_create_ad_unauthenticated(self):
        data = {
            "title": "Цветок 2",
            "price": 200,
        }
        url = reverse("advertisements:advertisement_create")
        response = self.client.post(url, data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Advertisement.objects.count() == 2

    def test_ads_list(self):
        url = reverse("advertisements:advertisements_list")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("count") == 2

    def test_user_ads_list(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse("advertisements:users_advertisements_list")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("count") == 1

        ad = Advertisement.objects.get(title="Ad 1")

        assert ad.title == "Ad 1"

    def test_retrieve_ad(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse(
            "advertisements:advertisement_retrieve", kwargs={"pk": self.ad1.pk}
        )

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Ad 1"

    def test_update_ad(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse("advertisements:advertisement_update", kwargs={"pk": self.ad1.pk})
        data = {"title": "Updated Ad 1", "price": 150}

        response = self.client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK

        self.ad1.refresh_from_db()

        assert self.ad1.title == "Updated Ad 1"
        assert self.ad1.price == 150

    def test_delete_ad(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse("advertisements:advertisement_delete", kwargs={"pk": self.ad1.pk})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Advertisement.objects.filter(pk=self.ad1.pk).exists()


@pytest.mark.django_db
class TestComment:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(email="user1@mail.ru", password="test")
        self.user2 = User.objects.create_user(email="user2@mail.ru", password="test")

        self.ad = Advertisement.objects.create(
            title="Test",
            price=100,
            author=self.user1,
        )
        self.comment1 = Comment.objects.create(
            text="Comment 1",
            advertisement=self.ad,
            author=self.user1,
        )
        self.comment2 = Comment.objects.create(
            text="Comment 2",
            advertisement=self.ad,
            author=self.user2,
        )

    def test_create_comment(self):
        self.client.force_authenticate(user=self.user1)

        data = {
            "text": "New comment",
        }
        url = reverse("advertisements:comment_create", kwargs={"ad_pk": self.ad.pk})
        response = self.client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.all().count() == 3

        new_comment = Comment.objects.get(text="New comment")

        assert new_comment.author == self.user1
        assert new_comment.advertisement == self.ad

    def test_create_comment_unauthenticated(self):
        url = reverse("advertisements:comment_create", kwargs={"ad_pk": self.ad.pk})
        data = {"text": "New comment"}
        response = self.client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Comment.objects.count() == 2

    def test_comments_list_for_ad(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse("advertisements:comments_list", kwargs={"ad_pk": self.ad.pk})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("count") == 2

    def test_comments_list_all(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse("advertisements:all_comments_list")

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("count") == 2

    def test_user_comments_list(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse("advertisements:users_comments_list")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("count") == 1

    def test_update_comment(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse(
            "advertisements:user_comment_update", kwargs={"pk": self.comment1.pk}
        )
        data = {"text": "Updated comment"}

        response = self.client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK
        self.comment1.refresh_from_db()
        assert self.comment1.text == "Updated comment"

    def test_delete_comment(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse(
            "advertisements:user_comment_delete", kwargs={"pk": self.comment1.pk}
        )

        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Comment.objects.filter(pk=self.comment1.pk).exists()
