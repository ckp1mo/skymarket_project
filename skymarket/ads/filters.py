import django_filters
from ads.models import Ad


class AdFilter(django_filters.FilterSet):
    """Простой фильтр осуществляет поиск по заголовку объявления"""
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', )

    class Meta:
        model = Ad
        fields = ('title', )
