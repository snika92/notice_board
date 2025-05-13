from django.urls import path
from rest_framework.permissions import AllowAny

from .apps import AdvertisementsConfig
from .views import (AdvertisementCreateApiView, AdvertisementDestroyApiView,
                    AdvertisementListApiView, AdvertisementRetrieveApiView,
                    AdvertisementUpdateApiView, AllCommentListApiView,
                    CommentCreateApiView, CommentDestroyApiView,
                    CommentListApiView, CommentUpdateApiView,
                    UsersAdvertisementListApiView, UsersCommentListApiView)

app_name = AdvertisementsConfig.name

urlpatterns = [
    path("", AdvertisementListApiView.as_view(permission_classes=(AllowAny,)), name="advertisements_list",),
    path("users_ads/", UsersAdvertisementListApiView.as_view(), name="users_advertisements_list",),
    path("<int:pk>/", AdvertisementRetrieveApiView.as_view(), name="advertisement_retrieve",),
    path("create/", AdvertisementCreateApiView.as_view(), name="advertisement_create"),
    path("<int:pk>/delete/", AdvertisementDestroyApiView.as_view(), name="advertisement_delete",),
    path("<int:pk>/update/", AdvertisementUpdateApiView.as_view(), name="advertisement_update",),

    path("all_comments/", AllCommentListApiView.as_view(), name="all_comments_list"),

    path("<int:ad_pk>/comments/", CommentListApiView.as_view(), name="comments_list"),
    path("<int:ad_pk>/comments/create/", CommentCreateApiView.as_view(), name="comment_create",),
    path("<int:ad_pk>/comments/<int:pk>/update/", CommentUpdateApiView.as_view(), name="comment_update",),
    path("<int:ad_pk>/comments/<int:pk>/delete/", CommentDestroyApiView.as_view(), name="comment_delete",),

    path("users_comments/", UsersCommentListApiView.as_view(), name="users_comments_list"),
    path("users_comments/<int:pk>/update/", CommentUpdateApiView.as_view(), name="user_comment_update",),
    path("users_comments/<int:pk>/delete/", CommentDestroyApiView.as_view(), name="user_comment_delete",),
]
