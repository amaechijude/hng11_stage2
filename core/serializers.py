from rest_framework import serializers
from .models import User, Organisation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):
        user = User(
            userId = validated_data['userId'],
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