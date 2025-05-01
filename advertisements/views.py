from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsAdmin, IsOwner

from .models import Advertisement, Review
from .paginators import CustomAdPagination, CustomReviewPagination
from .serializers import AdvertisementSerializer, ReviewSerializer


class AdvertisementCreateApiView(CreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAdmin | IsOwner, IsAuthenticated]

    def perform_create(self, serializer):
        new_ad = serializer.save()
        new_ad.owner = self.request.user
        new_ad.save()


class AdvertisementListApiView(ListAPIView):
    pagination_class = CustomAdPagination
    serializer_class = AdvertisementSerializer

    def get_queryset(self, *args, **kwargs):
        return Advertisement.objects.all()

    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ("created_at",)
    search_fields = ("title",)


class UsersAdvertisementListApiView(ListAPIView):
    pagination_class = CustomAdPagination
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return Advertisement.objects.filter(author=self.request.user.id)

    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ("created_at",)
    search_fields = ("title",)


class AdvertisementRetrieveApiView(RetrieveAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsOwner]


class AdvertisementUpdateApiView(UpdateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsOwner]


class AdvertisementDestroyApiView(DestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, ~IsAdmin | IsOwner]


class ReviewCreateApiView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdmin | IsOwner, IsAuthenticated]

    def perform_create(self, serializer):
        new_ad = serializer.save()
        new_ad.owner = self.request.user
        new_ad.save()


class ReviewListApiView(ListAPIView):
    pagination_class = CustomReviewPagination
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return Review.objects.all()


class ReviewRetrieveApiView(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsOwner]


class ReviewUpdateApiView(UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsOwner]


class ReviewDestroyApiView(DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, ~IsAdmin | IsOwner]
