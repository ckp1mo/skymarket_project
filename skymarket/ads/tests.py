from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User
from ads.models import Ad, Comment


class InitialAPITestCase(APITestCase):
    """Подготовка к тестам.
    Создание тестового пользователя, объявления, комментария"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            first_name='first_test', last_name='last_test', password='1234', phone='+77777777777',
            email='test@test.com', is_superuser='True'
        )
        self.ad = Ad.objects.create(title='first_ad', price=123, description='empty', author=self.user)
        self.comment = Comment.objects.create(text='first_comment', author=self.user, ad=self.ad)
        self.client.force_authenticate(user=self.user)


class AdAPITestCase(InitialAPITestCase):
    """Класс тестирования объявлений"""

    def test_create_ad(self):
        """Создание объявления"""

        data = {
            'title': 'unique_title',
            'price': 123456,
            'description': 'test_description',
            'author': self.user.pk
        }
        response = self.client.post('/api/ads/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Ad.objects.filter(title='unique_title').exists())

    def test_list_ad(self):
        """Просмотр всех объявлений"""

        response = self.client.get('/api/ads/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Ad.objects.all().count() == 1)

    def test_retrieve_ad(self):
        """Просмотр детальной информации объявления"""

        response = self.client.get(f'/api/ads/{self.ad.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_ad(self):
        """Редактирование объявления"""

        data = {
            'description': 'not_empty'
        }
        response = self.client.patch(f'/api/ads/{self.ad.pk}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['description'], data['description'])

    def test_delete_ad(self):
        """Удаление объявления"""

        response = self.client.delete(f'/api/ads/{self.ad.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentAPITestCase(InitialAPITestCase):
    """Класс тестирования комментариев"""

    def test_create_comment(self):
        """Создание комментария"""

        data = {
            'text': 'second_comment',
            'author': self.user.pk,
            'ad': self.ad.pk
        }
        response = self.client.post(f'/api/ads/{self.ad.pk}/comments/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(ad=self.ad).exists())

    def test_list_comment(self):
        """Просмотр всех комментариев к объявлению"""

        response = self.client.get(f'/api/ads/{self.ad.pk}/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), Comment.objects.filter(ad=self.ad).count())

    def test_retrieve_comment(self):
        """Просмотр комментария"""

        response = self.client.get(f'/api/ads/{self.ad.pk}/comments/{self.comment.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.comment.pk)

    def test_update_comment(self):
        """Редактирование комментария"""

        data = {
            'text': 'still first comment'
        }
        response = self.client.patch(f'/api/ads/{self.ad.pk}/comments/{self.comment.pk}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['text'], data['text'])

    def test_delete_comment(self):
        """Удаление комментария"""

        response = self.client.delete(f'/api/ads/{self.ad.pk}/comments/{self.comment.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

