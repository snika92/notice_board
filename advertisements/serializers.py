from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import User

from .models import Advertisement, Comment


class AdvertisementSerializer(ModelSerializer):
    author = SerializerMethodField()
    comments_count = SerializerMethodField()

    def get_author(self, advertisement):
        return [
            author.email for author in User.objects.filter(advertisements=advertisement)
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Advertisement
        fields = [
            "pk",
            "title",
            "price",
            "description",
            "author",
            "created_at",
            "comments_count",
        ]


class CommentSerializer(ModelSerializer):
    author = SerializerMethodField()
    advertisement = SerializerMethodField()

    def get_author(self, comment):
        return [author.email for author in User.objects.filter(comments=comment)]

    def get_advertisement(self, comment):
        return [
            advertisement.title
            for advertisement in Advertisement.objects.filter(comments=comment)
        ]

    class Meta:
        model = Comment
        fields = "__all__"
