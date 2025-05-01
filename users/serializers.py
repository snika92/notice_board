from rest_framework.serializers import ModelSerializer

from .models import User

from advertisements.serializers import AdvertisementSerializer, ReviewSerializer


class UserSerializer(ModelSerializer):
    advertisements = AdvertisementSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "password",
            "first_name",
            "last_name",
            "phone",
            "email",
            "role",
            "image",
            "advertisements",
            "reviews",
        ]


class UserDetailSerializer(ModelSerializer):
    advertisements = AdvertisementSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "image",
            "advertisements",
            "reviews",
        ]
