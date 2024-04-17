from django.urls import path
from rest_framework.routers import DefaultRouter
from ads.apps import SalesConfig
from ads.views import AdMyListAPIView, AdViewSet, CommentListCreateApiView, CommentRetrieveUpdateDeleteAPIView

router = DefaultRouter()
router.register(r'ads', AdViewSet, basename='ads')

app_name = SalesConfig.name

urlpatterns = [
    # Объявления
    path('ads/me/', AdMyListAPIView.as_view(), name='ads-my-list'),

    # Отзывы
    path('ads/<int:ad_pk>/comments/', CommentListCreateApiView.as_view(), name='comment-list'),
    path('ads/<int:ad_pk>/comments/<int:id>/', CommentRetrieveUpdateDeleteAPIView.as_view(),
         name='comment-retrieve-update-delete'),
    # path('ads/<int:ad_pk>/comments/', CommentCreateApiView.as_view(), name='comment-create'),
] + router.urls
