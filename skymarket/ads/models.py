from django.conf import settings
from django.db import models
from users.models import NULLABLE


class Ad(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название товара')
    price = models.PositiveIntegerField(verbose_name='Цена товара')
    description = models.TextField(max_length=1000, verbose_name='Описание товара')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    image = models.ImageField(upload_to='ads/', **NULLABLE, verbose_name='Изображение')

    def __str__(self):
        return f"{self.title}, {self.price}, {self.price}"

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='Объявления')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return f"{self.text[:20]}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
