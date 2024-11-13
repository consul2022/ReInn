from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.serializers import Serializer

from .models import User


class RegistrationSerializer(Serializer):
    phone = PhoneNumberField()
    password = serializers.CharField(min_length=8, write_only=True)
    repeat_password = serializers.CharField(min_length=8, write_only=True)
    last_name = serializers.CharField()
    first_name = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['repeat_password']:
            raise serializers.ValidationError('Пароли не матчатся')
        if User.objects.filter(phone_number=data['phone']).exists():
            raise serializers.ValidationError('Юзер с таким телефоном уже сидит в базе')
        return data

    def create(self, validated_data):
        validated_data.pop('repeat_password')

        user = User(
            phone_number=validated_data['phone'],
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
