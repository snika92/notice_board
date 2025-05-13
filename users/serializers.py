from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (CharField, EmailField, ModelSerializer,
                                        Serializer)

from advertisements.serializers import (AdvertisementSerializer,
                                        CommentSerializer)

from .models import User


class UserSerializer(ModelSerializer):
    advertisements = AdvertisementSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "pk",
            "password",
            "first_name",
            "last_name",
            "phone",
            "email",
            "role",
            "image",
            "advertisements",
            "comments",
        ]


class UserDetailSerializer(ModelSerializer):
    advertisements_count = SerializerMethodField()
    comments_count = SerializerMethodField()

    def get_advertisements_count(self, obj):
        return obj.advertisements.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = User
        fields = [
            "pk",
            "first_name",
            "last_name",
            "phone",
            "email",
            "image",
            "advertisements_count",
            "comments_count",
        ]


class UserResetPasswordSerializer(Serializer):

    email = EmailField()


class UserResetPasswordConfirmSerializer(Serializer):
    uid = CharField()
    token = CharField()
    new_password = CharField(
        style={"input_type": "password"}, min_length=8, write_only=True
    )
