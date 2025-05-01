from django.urls import path
from rest_framework.permissions import AllowAny

from .apps import AdvertisementsConfig
from .views import (AdvertisementCreateApiView, AdvertisementDestroyApiView,
                    AdvertisementListApiView, AdvertisementRetrieveApiView,
                    AdvertisementUpdateApiView, ReviewCreateApiView,
                    ReviewDestroyApiView, ReviewListApiView,
                    ReviewRetrieveApiView, ReviewUpdateApiView,
                    UsersAdvertisementListApiView)

app_name = AdvertisementsConfig.name

urlpatterns = [
    path(
        "",
        AdvertisementListApiView.as_view(permission_classes=(AllowAny,)),
        name="advertisements_list",
    ),
    path(
        "users_ads/",
        UsersAdvertisementListApiView.as_view(),
        name="users_advertisements_list",
    ),
    path(
        "<int:pk>/",
        AdvertisementRetrieveApiView.as_view(),
        name="advertisement_retrieve",
    ),
    path("create/", AdvertisementCreateApiView.as_view(), name="advertisement_create"),
    path(
        "<int:pk>/delete/",
        AdvertisementDestroyApiView.as_view(),
        name="advertisement_delete",
    ),
    path(
        "<int:pk>/update/",
        AdvertisementUpdateApiView.as_view(),
        name="advertisement_update",
    ),
    path("reviews/", ReviewListApiView.as_view(), name="reviews_list"),
    path("reviews/<int:pk>/", ReviewRetrieveApiView.as_view(), name="review_retrieve"),
    path("reviews/create/", ReviewCreateApiView.as_view(), name="review_create"),
    path(
        "reviews/<int:pk>/delete/", ReviewDestroyApiView.as_view(), name="review_delete"
    ),
    path(
        "reviews/<int:pk>/update/", ReviewUpdateApiView.as_view(), name="review_update"
    ),
]
