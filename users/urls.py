from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .apps import UsersConfig
from .views import (UserCreateAPIView, UserDestroyApiView, UserListApiView,
                    UserResetPasswordApiView, UserResetPasswordConfirmApiView,
                    UserSelfListApiView, UserUpdateApiView)

app_name = UsersConfig.name

urlpatterns = [
    path("", UserListApiView.as_view(), name="users_list"),
    path("user/", UserSelfListApiView.as_view(), name="user_retrieve"),
    path("<int:pk>/update/", UserUpdateApiView.as_view(), name="user_update"),
    path("<int:pk>/delete/", UserDestroyApiView.as_view(), name="user_delete"),

    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login",),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh",),

    path("reset_password/", UserResetPasswordApiView.as_view(), name="password_reset"),
    path("reset_password_confirm/", UserResetPasswordConfirmApiView.as_view(), name="password_reset_confirm",),
]
