from rest_framework.serializers import ModelSerializer

# from advertisement.serializers import AdvertisementSerializer

from .models import User


class UserSerializer(ModelSerializer):
    # advertisements = AdvertisementSerializer(many=True, read_only=True)

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
            # "advertisements",
        ]


class UserDetailSerializer(ModelSerializer):
    # advertisements = AdvertisementSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "image",
            # "advertisements",
        ]
