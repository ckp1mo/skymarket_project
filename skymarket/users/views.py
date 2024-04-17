from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.serializers import UserSerializer, UserChangePasswordSerializer


class UserCreateListAPIView(generics.ListCreateAPIView):
    """Класс для просмотра всех пользователей и создания пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        """Хэширование пароля"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserSelfRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Класс для просмотра и редактирования своего профиля"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Класс для детального просмотра профиля"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserChangePassword(generics.CreateAPIView):
    """Класс для смены пароля"""
    serializer_class = UserChangePasswordSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
