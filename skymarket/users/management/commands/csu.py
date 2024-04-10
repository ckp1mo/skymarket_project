from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@test.com',
            first_name='Admin',
            last_name='Testov',
            phone='+8123456789',
            role='admin',
            is_staff=True,
            is_superuser=True,
        )
        user.set_password('qwerty')
        user.save()
