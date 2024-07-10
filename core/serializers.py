from rest_framework import serializers
from .models import User, Organisation
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'email', 'password', 'phone']
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):
        user = User(
            # userId = validated_data['userId'],
            firstName = validated_data['firstName'],
            lastName = validated_data['lastName'],
            email = validated_data['email'],
            phone = validated_data['phone']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if user is None:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include "email" and "password"')

        data['user'] = user
        return data
