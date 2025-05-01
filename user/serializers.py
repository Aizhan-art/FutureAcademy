from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import MyUser


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = MyUser(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])  # хешируем пароль
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        trim_whitespace=False,
        write_only=True,
        required=True
    )

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not user:
                raise serializers.ValidationError({"detail": "Неверный логин или пароль"})
        else:
            raise serializers.ValidationError({'detail': 'Логин и пароль обязательные поля'})

        attrs['user'] = user
        return attrs