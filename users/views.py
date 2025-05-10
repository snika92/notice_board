from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     GenericAPIView, ListAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from config import settings

from .models import User
from .permissions import IsAdmin, IsUser
from .serializers import (UserDetailSerializer,
                          UserResetPasswordConfirmSerializer,
                          UserResetPasswordSerializer, UserSerializer)


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdmin]


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserSelfListApiView(ListAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdmin | IsUser]

    def get_queryset(self):
        queryset = User.objects.filter(pk=self.request.user.id)
        print(queryset)
        return queryset


class UserRetrieveApiView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdmin | IsUser]


class UserUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [~IsAdmin, IsUser]


class UserDestroyApiView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [~IsAdmin, IsUser]


User = get_user_model()


class UserResetPasswordApiView(GenericAPIView):
    serializer_class = UserResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                data={"detail": "Пользователь с таким email не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_url = f"http://127.0.0.1:8000/users/{uid}/{token}/"
        subject = "Сброс пароля"
        message = f"""
               Здравствуйте!

               Для сброса пароля перейдите по следующей ссылке:
               {reset_url}

               Если вы не запрашивали сброс пароля, проигнорируйте это письмо.

               С уважением,
               Notice Board
               """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response(
            data={"detail": "Ссылка для сброса пароля отправлена на ваш email"},
            status=status.HTTP_200_OK,
        )


class UserResetPasswordConfirmApiView(GenericAPIView):
    serializer_class = UserResetPasswordConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = urlsafe_base64_decode(serializer.validated_data["uid"]).decode()
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response(
                {"detail": "Неверная ссылка для сброса пароля"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not default_token_generator.check_token(
            user, serializer.validated_data["token"]
        ):
            return Response(
                {"detail": "Неверная ссылка для сброса пароля"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response({"detail": "Пароль успешно изменен"}, status=status.HTTP_200_OK)
