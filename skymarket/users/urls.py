from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateListAPIView, UserSelfRetrieveUpdateAPIView, UserRetrieveAPIView, UserChangePassword
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name


urlpatterns = [
    # Юзер эндпоинты
    path('users/', UserCreateListAPIView.as_view(), name='user-create-list'),
    path('users/me/', UserSelfRetrieveUpdateAPIView.as_view(), name='userself-retrieve-update'),
    path('users/<int:pk>', UserRetrieveAPIView.as_view(), name='user-retrieve'),
    path('users/set_password/', UserChangePassword.as_view(), name='user-change-pass'),
    # авторизация
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
