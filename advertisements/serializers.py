from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import User

from .models import Advertisement, Review


class AdvertisementSerializer(ModelSerializer):
    owner = SerializerMethodField()

    def get_owner(self, advertisement):
        return [
            owner.email for owner in User.objects.filter(adverticements=advertisement)
        ]

    class Meta:
        model = Advertisement
        fields = "__all__"


class ReviewSerializer(ModelSerializer):
    owner = SerializerMethodField()

    def get_owner(self, review):
        return [owner.email for owner in User.objects.filter(reviews=review)]

    class Meta:
        model = Review
        fields = "__all__"
