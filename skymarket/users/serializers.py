from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserChangePasswordSerializer(serializers.Serializer):

    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def save(self, **kwargs):
        old_pass = self.validated_data.get('current_password')
        new_pass = self.validated_data.get('new_password')
        user = self.context['request'].user

        if check_password(old_pass, user.password):
            user.set_password(new_pass)
            user.save()
        else:
            raise ValidationError('Старый пароль указан неверно')
