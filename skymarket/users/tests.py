from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User


class UserAPITestCase(APITestCase):
    """Тестирование создание пользователя"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            first_name='first_test', last_name='last_test', phone='+77777777777',
            email='test@test.com', is_superuser='True'
        )
        self.user.set_password('1234')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        """Создание пользователя"""

        data = {
            'first_name': 'Ekaterina',
            'last_name': 'Repina',
            'password': 'qwerty',
            'phone': '+79999999999',
            'email': 'e.repina@test.com'
        }
        response = self.client.post('/api/users/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.all().exists())

    def test_update_user(self):
        """Редактирование пользователя"""

        data = {
            'first_name': 'Darya',
            'last_name': 'Razumova'
        }
        response = self.client.patch('/api/users/me/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['first_name'], data['first_name'])
        self.assertEqual(response.json()['last_name'], data['last_name'])

    def test_retrieve_user(self):
        """Получение информации о текущем пользователе"""

        response = self.client.get(f'/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['first_name'], self.user.first_name)

    def test_change_pass(self):
        """Изменение пароля"""

        data = {
            'current_password': '1234',
            'new_password': 'qwerty'
        }
        response = self.client.post('/api/users/set_password/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(check_password(data['new_password'], self.user.password))

    def test_list_user(self):
        """Просмотр всех пользователей"""

        # Создание дополнительного пользователя
        self.test_create_user()

        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), len(User.objects.all()))
