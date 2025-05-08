from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsAdmin, IsOwner

from .models import Advertisement, Comment
from .paginators import CustomAdPagination, CustomCommentPagination
from .serializers import AdvertisementSerializer, CommentSerializer


class AdvertisementCreateApiView(CreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_advertisement = serializer.save()
        new_advertisement.author = self.request.user
        new_advertisement.save()


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
    permission_classes = [IsAuthenticated]


class AdvertisementUpdateApiView(UpdateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsOwner]


class AdvertisementDestroyApiView(DestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsOwner]


class CommentCreateApiView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        ad_id = self.kwargs['ad_pk']
        ad = Advertisement.objects.get(pk=ad_id)

        new_comment = serializer.save()
        new_comment.author = self.request.user

        new_comment.advertisement = ad

        new_comment.save()


class CommentListApiView(ListAPIView):
    pagination_class = CustomCommentPagination
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        ad_pk = self.kwargs['ad_pk']
        return Comment.objects.filter(advertisement_id=ad_pk)


class AllCommentListApiView(ListAPIView):
    queryset = Comment.objects.all()
    pagination_class = CustomCommentPagination
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [OrderingFilter]
    ordering_fields = ("created_at",)


class UsersCommentListApiView(ListAPIView):
    pagination_class = CustomCommentPagination
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return Comment.objects.filter(author=self.request.user.id)

    filter_backends = [OrderingFilter]
    ordering_fields = ("created_at",)


class CommentUpdateApiView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsOwner]


class CommentDestroyApiView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsOwner]
