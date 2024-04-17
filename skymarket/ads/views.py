from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets, generics
from ads.serializers import AdSerializer, CommentSerializer
from ads.models import Ad, Comment
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from ads.filters import AdFilter
from rest_framework.permissions import IsAuthenticated
from ads.permissions import UserPermission


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    """ViewsSet для работы с объявлениями.
    Поддержка всех видов запросов get, post, put/patch, update, delete"""
    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = AdFilter
    permission_classes = [UserPermission]

    def perform_update(self, serializer):
        """Редактирование возможно, если пользователь является автором или администратором"""
        ad = serializer.save()
        if (ad.author != self.request.user) and (self.request.user.role != 'admin'):
            raise ValidationError('Недостаточно прав')

    def perform_create(self, serializer):
        """Привязка пользователя в поле автора при создании комментария"""
        new_ad = serializer.save()
        new_ad.author = self.request.user
        new_ad.save()

    def perform_destroy(self, instance):
        """Удаление возможно, если пользователь является автором или администратором"""
        ad = self.get_object()
        if (ad.author != self.request.user) and (self.request.user.role != 'admin'):
            raise ValidationError('Недостаточно прав')
        instance.delete()


class AdMyListAPIView(generics.ListAPIView):
    """Список моих объявлений"""
    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    pagination_class = AdPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class CommentListCreateApiView(generics.ListCreateAPIView):
    """Объединенный класс для создания и просмотра всех комментариев.
    Для создания используйте post запрос
    Для просмотра используйте get запрос"""
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Просмотр всех комментариев к выбранному объявлению"""
        return Comment.objects.filter(ad=self.kwargs.get('ad_pk'))

    def perform_create(self, serializer):
        """Привязка автора и объявления при создании комментария"""
        new_comment = serializer.save()
        ad_pk = self.kwargs.get('ad_pk')
        new_comment.author = self.request.user
        new_comment.ad_id = ad_pk
        new_comment.save()


class CommentRetrieveUpdateDeleteAPIView(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    """Объединенный класс для просмотра, изменения и удаления комментариев.
    Для просмотра данных о комментарии используйте get запрос.
    Для изменения данных используйте patch запрос.
    Для удаления используйте delete запрос"""
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Детальный просмотр комментария"""
        ad_pk = self.kwargs.get('ad_pk')
        comment_id = self.kwargs.get('id')
        return get_object_or_404(Comment, pk=comment_id, ad=ad_pk)

    def perform_update(self, serializer):
        """Редактирование возможно, если пользователь является автором или администратором"""
        ad = serializer.save()
        if (ad.author != self.request.user) and (self.request.user.role != 'admin'):
            raise ValidationError('Недостаточно прав')

    def perform_destroy(self, instance):
        """Удаление возможно если пользователь является автором или администратором"""
        ad = self.get_object()
        if (ad.author != self.request.user) and (self.request.user.role != 'admin'):
            raise ValidationError('Недостаточно прав')
        instance.delete()
